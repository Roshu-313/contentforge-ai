# ⚡ ContentForge AI
### Autonomous Multi-Agent Content Intelligence System

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![CrewAI](https://img.shields.io/badge/CrewAI-1.14-green)](https://crewai.com)
[![Groq](https://img.shields.io/badge/LLM-Groq%20LLaMA%203.3-orange)](https://groq.com)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-teal)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 🚀 What is ContentForge AI?

ContentForge AI is a **production-ready, multi-agent content automation system** built with CrewAI. Give it any topic and it autonomously researches the web, analyzes trends, writes a full SEO-optimized blog post, and generates platform-native social media posts — all in one pipeline.

Built as a real-world alternative to expensive content agencies and generic AI writing tools. **No OpenAI required. Runs on free-tier APIs.**

---

## ✨ Features

- 🤖 **3 specialized AI agents** — Researcher, Writer, Reviewer
- 🔍 **Real-time web research** via Serper API (Google search)
- 📝 **Full markdown blog post** (600-800 words, SEO-optimized)
- 📱 **Platform-native social posts** — LinkedIn, Twitter/X, Instagram
- 💾 **Content saved to SQLite** database automatically
- 🚀 **FastAPI REST endpoint** — integrate with any system
- 🖥️ **Streamlit UI** — clean no-code interface for clients
- 💸 **100% free-tier compatible** — Groq + Together AI + Serper
- ⚡ **Ultra-fast inference** via Groq (LLaMA 3.3 70b)
- 🔒 **Structured Pydantic output** — API-ready JSON every time

---

## 🏗️ Architecture

### Agent Pipeline (Sequential)

```
[Researcher] → [Writer] → [Reviewer] → JSON Output
```

| Agent | Model | Role | Tools |
|---|---|---|---|
| Senior Research Analyst | Groq LLaMA 3.3 70b | Searches web, gathers news + trends | SerperDevTool ✅ |
| Expert Content Writer | Groq LLaMA 3.3 70b| Writes blog post + social media posts | None ❌ |
| Chief Content Officer | Groq LLaMA 3.3 70b | Reviews and returns structured output | None ❌ |

### Why This Architecture?
- **Only 1 agent has search tools** — eliminates token overflow and tool call errors
- **Writer works from context** — faster, more focused output
- **Pydantic output enforcement** — structured JSON every single time

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Agent Framework | CrewAI 1.14 |
| LLM (Research + Review) | Groq — LLaMA 3.3 70b Versatile |
| LLM (Writing) | Groq — LLaMA 3.3 70b Versatile|
| Web Search | Serper API |
| Backend API | FastAPI |
| Frontend | Streamlit |
| Database | SQLite + SQLAlchemy |
| Data Validation | Pydantic v2 |
| Logging | Loguru |

---

## 📁 Project Structure

```
contentforge-ai/
├── config/
│   ├── agents.yaml          # Agent definitions (legacy, kept for reference)
│   └── tasks.yaml           # Task definitions (legacy, kept for reference)
├── backend/
│   ├── main.py              # FastAPI app + /generate + /history endpoints
│   ├── models.py            # SQLAlchemy DB models
│   └── schemas.py           # Pydantic schemas
├── database/
│   └── db.py                # DB connection + session management
├── frontend/
│   └── app.py               # Streamlit UI
├── logs/                    # Auto-generated log files
├── main_crew.py             # Core crew logic — agents, tasks, execution
├── .env                     # API keys (never commit this)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/contentforge-ai
cd contentforge-ai
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up API keys
Create a `.env` file:
```env
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
OPENAI_API_KEY=sk-fake-not-needed-123
```

| Key | Where to get | Cost |
|---|---|---|
| GROQ_API_KEY | console.groq.com | Free |
| SERPER_API_KEY | serper.dev | Free (2500/month) |

### 5. Run the system

**Terminal 1 — Backend:**
```bash
python -m uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
streamlit run frontend/app.py
```

**Or run crew directly:**
```bash
python main_crew.py
```

---

## 🌐 API Usage

### Generate Content
```http
POST /generate
Content-Type: application/json

{
  "subject": "AI tools for freelancers in 2026"
}
```

### Response
```json
{
  "id": 1,
  "subject": "AI tools for freelancers in 2026",
  "word_count": 743,
  "article": "# AI Tools for Freelancers...",
  "social_media_posts": [
    {"platform": "LinkedIn", "content": "..."},
    {"platform": "Twitter",  "content": "..."},
    {"platform": "Instagram","content": "..."}
  ]
}
```

### Get History
```http
GET /history
```

### Interactive API Docs
```
http://localhost:8000/docs
```

---

## 💡 How It Works

```
User enters topic
      ↓
[Researcher Agent — Groq]
  • Searches web via Serper API
  • Finds top 3 news items
  • Identifies market trends
  • Extracts SEO keywords
  • Returns 400-word research brief
      ↓
[Writer Agent — Together AI Mixtral]
  • Receives research brief as context
  • Writes 600-800 word SEO blog post
  • Creates LinkedIn, Twitter, Instagram posts
  • Never calls any external tools
      ↓
[Reviewer Agent — Groq]
  • Reviews full content package
  • Ensures markdown formatting
  • Validates platform-specific tone
  • Returns structured Pydantic output
      ↓
FastAPI saves to SQLite + returns JSON
      ↓
Streamlit displays blog post + social posts
```

---

## 🎯 Use Cases

- **Marketing agencies** — automate content pipelines for multiple clients
- **SaaS founders** — thought leadership content at scale
- **Freelance writers** — 10x output with AI-assisted research
- **E-commerce brands** — product-niche blog content automation
- **Newsletter operators** — weekly research + writing automation

---

## 🔑 Why This Stands Out

| Basic AI Project | ContentForge AI |
|---|---|
| Single ChatGPT prompt | 3 specialized agents with defined roles |
| Hallucinates facts | Real-time web research via Serper |
| Generic output | Pydantic-structured JSON — API-ready |
| OpenAI dependency | Groq + Together AI — free tier |
| No persistence | SQLite DB — full content history |
| Terminal only | FastAPI + Streamlit — client-presentable |
| One provider | Multi-provider — spreads rate limits |

---

## 📦 Requirements

```
crewai[tools]
fastapi
uvicorn
streamlit
sqlalchemy
python-dotenv
pydantic
loguru
together
litellm
```

---

## 🤝 Contributing

Pull requests welcome! For major changes please open an issue first.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👤 Author

Built by Roshan Faisal — AI Automation Engineer

[![GitHub](https://img.shields.io/badge/GitHub-yourprofile-black)](https://github.com/Roshu-313)
[![Upwork](https://img.shields.io/badge/Upwork-hire%20me-green)](https://www.upwork.com/freelancers/~012d6babc78416f699)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-connect-blue)](https://www.linkedin.com/in/roshan-faisal-9662742b0/)

---

*ContentForge AI — Because great content shouldn't take all day.*
