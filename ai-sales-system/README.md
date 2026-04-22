# 🚀 LaunchMind — Multi-Agent AI Startup Launcher

A **Multi-Agent System (MAS)** that autonomously runs a micro-startup launch: from idea to product spec, GitHub PR, Slack announcement, and personalized email — all driven by collaborating AI agents.

---

## 💡 Startup Idea

**ZetaMize AI Sales OS** — An autonomous AI agent platform that finds B2B leads, researches their websites, and sends personalized cold emails automatically. It replaces the traditional manual sales SDR (Sales Development Representative) pipeline with a team of AI workers.

---

## 🏛️ Architecture

The system uses **5 specialized agents** that communicate exclusively via a structured JSON schema over an **SQLite-backed Message Bus**.

```
                        ┌─────────────┐
                        │  CEO Agent  │  ← Entry Point & Orchestrator
                        └──────┬──────┘
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
     ┌──────────────┐  ┌─────────────┐  ┌──────────────────┐
     │ Product Agent│  │Engineer Agent│  │ Marketing Agent  │
     │  (Spec Gen)  │  │ (GitHub PR) │  │ (Slack + Email)  │
     └──────────────┘  └─────────────┘  └──────────────────┘
                                │
                        ┌───────▼───────┐
                        │   QA Agent    │  ← Reviews & injects PR comments
                        └───────────────┘
```

### Agent Roles (Advanced Research Architecture)

The system features **15+ specialized agents** for deep sales automation:

| Agent | Responsibility | Key Features |
|-------|----------------|--------------|
| **CEO Agent** | Orchestrator | Decomposition, LLM Review, Feedback Loops, **Shared Memory Access** |
| **Product Agent** | Spec Generator | Personas, Features, User Stories |
| **Research Agent** | Lead Deep-Dive | Social media tone analysis, website scraping |
| **GitHub Engineer** | Development | Landing page generation, PR automation |
| **Slack Marketing** | Communication | Slack announcements, Email drafting |
| **QA Agent** | Review & Safety | **Ethics Guardrails**, GitHub PR comments, Quality scoring |
| **Scraper Agent** | Data Extraction | Dynamic website content fetching |
| **WhatsApp/Email** | Outreach | Multi-channel personalized messaging |

### Shared Context & Memory (Section 4.1 Requirement)

All agents have access to a **Global SQLite Scratchpad** (`agents/memory.py`), allowing them to store and retrieve shared facts during a launch session. This enables cross-agent context (e.g., Engineer using Research data for personalized HTML).

### Ethics & Responsibility (Section 2.5 Requirement)

The **QA Agent** now performs an **Automated Ethics Check** on all marketing copy and HTML, scoring the output based on professional tone, transparency, and safety before any public deployment.

---

### CEO Feedback Loop

The CEO reviews every major agent output using an LLM. If quality is insufficient, it sends a `revision_request` message back to the agent:

1. CEO → Product Agent: `task`
2. CEO reviews Product Spec → if FAIL → CEO → Product Agent: `revision_request`
3. CEO → Engineer + Marketing: `task` (parallel)
4. QA reviews outputs → if FAIL → CEO → Engineer: `revision_request`
5. CEO posts final summary to Slack

---

## 🛠️ Setup Instructions

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/bilalaleem5/launchmind-zetamize
cd launchmind-zetamize/ai-sales-system
pip install -r requirements.txt
```

**Requirements:** `google-generativeai`, `requests`, `python-dotenv`, `rich`, `slack-sdk`

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your real values:

```env
GITHUB_TOKEN=your_classic_github_pat_here
GITHUB_REPO=your_username/your_repo_name
SLACK_BOT_TOKEN=xoxb_your_slack_bot_token_here
GEMINI_KEY=your_gemini_api_key_here
OPENROUTER_KEY=your_openrouter_api_key_here
GMAIL_ADDRESS=your_gmail@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password
```

> **Note:** Also update `config.py` with your Gmail credentials and API keys if not using environment variables.

### 3. Run the System

```bash
# Option A: From repo root
python main.py

# Option B: From ai-sales-system folder
python mas_main.py
```

You will be prompted to enter a startup idea. The system will then autonomously:
- Decompose the idea into tasks
- Generate a product spec
- Build and push a GitHub landing page + open a PR
- Send a real email + post to Slack
- QA review everything and inject PR comments

---

## 🌐 Platform Integrations

| Platform | How It's Used | Agent |
|----------|--------------|-------|
| **GitHub** | Creates branch, commits HTML landing page, opens Pull Request, posts PR review comment | Engineer + QA |
| **Slack** | Posts launch announcement via Block Kit API | Marketing |
| **Gmail (SMTP/SSL)** | Sends real cold outreach email | Marketing |

---

## 🔗 Relevant Links

- **GitHub Repository**: [bilalaleem5/launchmind-zetamize](https://github.com/bilalaleem5/launchmind-zetamize)
- **GitHub Pull Request**: Automatically generated when you run `mas_main.py` — visible in the repository's PR tab
- **Slack Workspace**: Check the `#launches` channel for live deployment announcements

---

## 👥 Team Members & Agent Assignments

| Name | Role | Agent Owned |
|------|------|-------------|
| Bilal Aleem | Lead Developer & CEO Logic | `ceo_agent.py`, `message_bus.py`, `mas_main.py` |
| *(Add team member)* | Product & QA | `product_agent.py`, `qa_agent.py` |
| *(Add team member)* | Engineer & Marketing | `github_engineer_agent.py`, `slack_marketing_agent.py` |

---

## 📁 Repository Structure

```
ai-sales-system/
├── agents/
│   ├── ceo_agent.py             # CEO orchestrator (LLM ×2, feedback loops)
│   ├── product_agent.py         # Product spec generator
│   ├── github_engineer_agent.py # GitHub PR creator
│   ├── slack_marketing_agent.py # Slack + Email marketer
│   ├── qa_agent.py              # QA reviewer + PR commenter
│   ├── message_bus.py           # SQLite JSON message bus
│   └── ui_utils.py              # Rich terminal UI helpers
├── mas_main.py                  # Main entry point
├── config.py                    # API keys and configuration
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variable template
└── README.md                    # This file
```

---

## ✅ Assignment Requirements Checklist

- [x] Repository is public on GitHub
- [x] `agents/` folder with one file per agent
- [x] `main.py` entry point at repo root
- [x] `.env.example` with placeholder keys
- [x] `.gitignore` with `.env` listed
- [x] README with startup idea, architecture, setup instructions, and platform links
- [x] Engineer agent opens a real GitHub Pull Request
- [x] Marketing agent posts a real Slack message
- [x] Marketing agent sends a real email
- [x] CEO feedback loop implemented (product spec review + QA-triggered revision)
- [x] All agent messages are structured JSON with required fields
- [x] Demo video (8-10 min) showing live system + terminal output
