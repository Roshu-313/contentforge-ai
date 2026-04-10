import os
import yaml
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from pydantic import BaseModel
from typing import List
from loguru import logger

load_dotenv()


# ------------------ OUTPUT MODELS ------------------ #

class SocialMediaPost(BaseModel):
    platform: str
    content: str


class ContentOutput(BaseModel):
    article: str
    social_media_posts: List[SocialMediaPost] = []
    subject: str = ""
    word_count: int = 0


# ------------------ CONFIG LOADER ------------------ #

def load_configs():
    with open("config/agents.yaml", "r") as f:
        agents_cfg = yaml.safe_load(f)
    with open("config/tasks.yaml", "r") as f:
        tasks_cfg = yaml.safe_load(f)
    return agents_cfg, tasks_cfg


# ------------------ MAIN FUNCTION ------------------ #

def run_content_crew(subject: str) -> ContentOutput:
    logger.info(f"Starting ContentForge AI for subject: {subject}")

    search_tool = SerperDevTool()

    # ─── Model Strategy ───────────────────────────────────────────────────
    #
    #  AGENT 1 — Researcher
    #  Model  : Groq llama-3.1-70b
    #  Job    : Search web, gather news + trends
    #  Tools  : SerperDevTool ✅
    #
    #  AGENT 2 — Writer
    #  Model  : Together AI Mixtral-8x7b
    #  Job    : Write blog post + social media posts
    #  Tools  : None ❌
    #
    #  AGENT 3 — Reviewer
    #  Model  : Groq llama-3.3-70b
    #  Job    : Review and return structured output
    #  Tools  : None ❌
    #
    # ──────────────────────────────────────────────────────────────────────

    llm_researcher = "groq/llama-3.3-70b-versatile"
    llm_writer = "groq/llama-3.3-70b-versatile"
    llm_reviewer   = "groq/llama-3.3-70b-versatile"


    # ------------------ AGENTS ------------------ #

    researcher = Agent(
        role="Senior Research Analyst",
        goal=f"Research the latest news, trends, and data about {subject}. "
             f"Provide a comprehensive research report covering key news, "
             f"market trends, statistics, and SEO keywords.",
        backstory="You are an expert researcher and market analyst. "
                  "You search the web efficiently, extract the most "
                  "relevant information, and produce clear research briefs "
                  "that writers can use directly.",
        tools=[search_tool],
        llm=llm_researcher,
        allow_delegation=False,
        verbose=True,
        max_iter=2,
    )

    writer = Agent(
        role="Expert Content Writer and SEO Strategist",
        goal=f"Using the research provided, write a complete content package "
             f"about {subject}: a full SEO-optimized blog post in markdown "
             f"plus LinkedIn, Twitter, and Instagram posts.",
        backstory="You are a world-class content writer who blends SEO "
                  "expertise with compelling storytelling. You write "
                  "blog posts that rank on Google and social posts that "
                  "get engagement. You never need to search — you work "
                  "from the research given to you.",
        llm=llm_writer,
        allow_delegation=False,
        verbose=True,
        max_iter=1,
    )

    reviewer = Agent(
        role="Chief Content Officer",
        goal="Review the content package and return it as a perfectly "
             "structured output with the article and all social media posts.",
        backstory="You are the final quality gate. You ensure the content "
                  "is well-formatted in markdown, the social posts match "
                  "their platforms, and everything is structured correctly "
                  "for the API response.",
        llm=llm_reviewer,
        allow_delegation=False,
        verbose=True,
        max_iter=1,
    )


    # ------------------ TASKS ------------------ #

    task_research = Task(
        description=f"""
        Search the web and research everything about: {subject}

        Your research report MUST include:
        1. Top 3 latest news items with source and key insight
        2. Key market trends and data points
        3. Primary keyword and 5 SEO-friendly secondary keywords
        4. Target audience and their main pain points
        5. 3 compelling content angles

        Keep your report concise — max 400 words.
        """,
        expected_output="""
        A structured research report with:
        - 3 news items (title, source, insight)
        - 3 market trends with data
        - Primary keyword + 5 secondary keywords
        - Target audience description
        - 3 content angles
        """,
        agent=researcher,
    )

    task_write = Task(
        description=f"""
        Using ONLY the research report provided in context, create a
        complete content package about: {subject}

        Write:
        1. A blog post (600-800 words) in markdown with:
           - SEO-optimized H1 title
           - Introduction (hook the reader)
           - 3 main sections with H2 headings
           - Conclusion with CTA
           - Primary keyword used naturally

        2. LinkedIn post (150 words, professional tone, no emojis)
        3. Twitter/X post (under 280 chars, punchy, 2 hashtags)
        4. Instagram caption (fun tone, 3-5 hashtags)

        DO NOT search the web. Use only the research given.
        """,
        expected_output="""
        Complete content package:
        - Full markdown blog post
        - LinkedIn post
        - Twitter post
        - Instagram caption
        """,
        agent=writer,
        context=[task_research],
    )

    task_review = Task(
        description=f"""
        Review the content package about {subject} and return it
        as a structured output.

        Make sure:
        - Blog post is properly formatted in markdown
        - Each social post matches its platform tone
        - No repetitive or filler content
        - Article is complete with introduction and conclusion

        Return the final structured content package.
        """,
        expected_output="""
        Final content package with article in markdown and
        social_media_posts list with platform and content fields.
        """,
        agent=reviewer,
        context=[task_write],
        output_pydantic=ContentOutput,
    )


    # ------------------ CREW ------------------ #

    crew = Crew(
        agents=[researcher, writer, reviewer],
        tasks=[task_research, task_write, task_review],
        process=Process.sequential,
        verbose=True,
        max_rpm=3,
    )


    # ------------------ EXECUTION ------------------ #

    try:
        result = crew.kickoff(inputs={"subject": subject})
    except Exception as e:
        logger.error(f"Crew failed: {e}")
        return ContentOutput(
            article=f"Generation failed: {str(e)}",
            subject=subject,
            word_count=0
        )


    # ------------------ OUTPUT HANDLING ------------------ #

    try:
        output = result.pydantic
        if output is None:
            raise ValueError("Pydantic output is None")

        output.word_count = len(output.article.split())
        output.subject = subject

    except Exception as e:
        logger.warning(f"Pydantic parsing failed: {e} — using raw output")
        raw = result.raw if result.raw else ""
        output = ContentOutput(
            article=raw,
            social_media_posts=[],
            subject=subject,
            word_count=len(raw.split())
        )

    logger.success(f"Done! Word count: {output.word_count}")
    return output


# ------------------ RUN ------------------ #

if __name__ == "__main__":
    result = run_content_crew("AI tools for freelancers in 2026")
    print(result.article)