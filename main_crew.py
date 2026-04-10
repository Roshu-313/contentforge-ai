import os
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


# ------------------ MAIN FUNCTION ------------------ #

def run_content_crew(subject: str) -> ContentOutput:
    logger.info(f"Starting ContentForge AI for subject: {subject}")

    search_tool = SerperDevTool()

    llm_researcher = "groq/llama-3.3-70b-versatile"
    llm_writer     = "groq/llama-3.3-70b-versatile"
    llm_reviewer   = "groq/llama-3.3-70b-versatile"


    # ------------------ AGENTS ------------------ #

    researcher = Agent(
        role="Senior Research Analyst",
        goal=f"Research latest info about {subject} using search tool.",
        backstory="Expert researcher. Uses search tool to find real information.",
        tools=[search_tool],
        llm=llm_researcher,
        allow_delegation=False,
        verbose=True,
        max_iter=2,
    )

    writer = Agent(
        role="Expert Content Writer",
        goal=f"Write engaging content about {subject} using provided research.",
        backstory="World class content writer. Uses only the research given.",
        llm=llm_writer,
        allow_delegation=False,
        verbose=True,
        max_iter=1,
    )

    reviewer = Agent(
        role="Content Reviewer",
        goal="Review and return the final structured content output.",
        backstory="Quality reviewer who formats output properly.",
        llm=llm_reviewer,
        allow_delegation=False,
        verbose=True,
        max_iter=1,
    )


    # ------------------ TASKS ------------------ #

    task_research = Task(
        description=f"""
        Research about: {subject}

        Use the search tool to find real information.

        Provide:
        - 3 key news items with source
        - 3 market trends
        - 5 SEO keywords
        - Target audience description
        """,
        expected_output="""
        A research report with:
        - 3 news items (title, source, insight)
        - 3 market trends
        - 5 SEO keywords
        - Target audience description
        Maximum 400 words.
        """,
        agent=researcher,
    )

    task_write = Task(
        description=f"""
        Using ONLY the research provided in context, write:

        1. Blog post (600-800 words) in markdown with:
           - SEO optimized H1 title
           - Introduction
           - 3 sections with H2 headings
           - Conclusion with CTA

        2. LinkedIn post (150 words, professional tone)
        3. Twitter post (under 280 chars, 2 hashtags)
        4. Instagram caption (fun tone, 3-5 hashtags)

        DO NOT search the web. Use only the research given.
        """,
        expected_output="""
        Complete content package:
        - Full markdown blog post (600-800 words)
        - LinkedIn post (150 words)
        - Twitter post (under 280 chars)
        - Instagram caption with hashtags
        """,
        agent=writer,
        context=[task_research],
    )

    task_review = Task(
        description=f"""
        Review the content package about {subject}.

        Make sure:
        - Blog post is properly formatted in markdown
        - Each social post matches its platform tone
        - Content is complete with intro and conclusion

        Return the final structured content package.
        """,
        expected_output="""
        Final content package with:
        - article: full markdown blog post
        - social_media_posts: list with platform and content for
          LinkedIn, Twitter and Instagram
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
        max_rpm=2,
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
        logger.warning(f"Pydantic parsing failed: {e}")
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