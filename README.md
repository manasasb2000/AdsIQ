# 🎯 AdsIQ — Google Ads API Intelligence Platform

> **Built by**: Manasa Samaga  
> **Targeting**: Product Solutions Engineer, Ads API @ Google  
> **Stack**: Next.js 14 · FastAPI · LangGraph · PostgreSQL · Redis · Docker

An AI-powered, multi-agent platform that simulates and automates the work of a Google Ads API Product Solutions Engineer — from troubleshooting API errors to building full campaign structures.

---

## 🚀 Quick Start

```bash
# Clone and enter the project
git clone <your-repo>
cd AI_Ads_Agent

# Copy environment variables
cp .env.example .env

# Start everything with Docker
docker compose up --build
```

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🤖 The 6 AI Agents

| Agent | Role |
|-------|------|
| 🔧 Troubleshooter | Diagnoses Google Ads API errors, generates code fixes |
| 🏗️ Campaign Builder | Builds full campaign hierarchies from a business brief |
| 🎨 Creative | Generates RSA headlines, descriptions, ad assets |
| 📊 Analytics | GAQL queries, ROAS/CTR/Quality Score analysis |
| 💬 Solutions Consultant | Customer-facing AI advisor |
| 🔄 Orchestrator | Supervisor that routes tasks between agents |

---

## 📁 Project Structure

```
AI_Ads_Agent/
├── frontend/        # Next.js 14 + TypeScript + Tailwind
├── backend/         # FastAPI + LangGraph + Python
├── docker/          # Docker Compose configuration
├── docs/            # Architecture & API documentation
└── .env.example     # Environment variables template
```

---

## 🛠️ Tech Stack

**Frontend**: Next.js 14, TypeScript, Tailwind CSS, shadcn/ui, Framer Motion, Recharts, Monaco Editor  
**Backend**: FastAPI, LangGraph, LangChain, SQLAlchemy, Alembic, Celery  
**AI/ML**: OpenAI GPT-4o, Google Gemini Pro  
**Database**: PostgreSQL + pgvector, Redis  
**Infrastructure**: Docker, Docker Compose, Nginx  

---

## 📖 Documentation

- [Architecture Overview](./docs/ARCHITECTURE.md)
- [Google Ads API Guide](./docs/GOOGLE_ADS_API_GUIDE.md)
- [Agent Workflows](./docs/AGENT_WORKFLOWS.md)
- [API Reference](http://localhost:8000/docs)
