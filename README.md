<div align="center">

<h1>
  <img src="https://raw.githubusercontent.com/manasasb2000/AdsIQ/main/frontend/public/favicon.ico" width="52" alt="AdsIQ Logo" onerror="this.src='https://img.icons8.com/color/96/google-ads.png'"><br>
  AdsIQ
</h1>

### The AI-Powered Google Ads API Intelligence Platform & Operational Control Plane

*Diagnose API errors, parse GAQL queries, generate compliant RSA creatives, and orchestrate stateful multi-agent campaign workflows.*

<p>
  <img src="https://img.shields.io/badge/API-TROUBLESHOOTER-4285F4?style=for-the-badge" alt="API Troubleshooter">
  <img src="https://img.shields.io/badge/GAQL-ENGINE-34A853?style=for-the-badge" alt="GAQL Engine">
  <img src="https://img.shields.io/badge/LANGGRAPH-ORCHESTRATOR-FBBC05?style=for-the-badge" alt="LangGraph Orchestrator">
  <img src="https://img.shields.io/badge/RSA-COMPLIANCE-EA4335?style=for-the-badge" alt="RSA Compliance">
  <img src="https://img.shields.io/badge/WEBSOCKET-STREAMING-7357FF?style=for-the-badge" alt="WebSocket Streaming">
</p>

<p>
  <img src="https://img.shields.io/badge/Next.js-14-000000?style=flat&logo=nextdotjs&logoColor=white" alt="Next.js 14">
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=flat&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white" alt="Python 3.12">
  <img src="https://img.shields.io/badge/TypeScript-5-3178C6?style=flat&logo=typescript&logoColor=white" alt="TypeScript 5">
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql&logoColor=white" alt="PostgreSQL 16">
  <img src="https://img.shields.io/badge/Redis-7-DC382D?style=flat&logo=redis&logoColor=white" alt="Redis 7">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat" alt="MIT License">
</p>

<p>
  <a href="#product-film">Product film</a> ·
  <a href="#product-workflow">Product workflow</a> ·
  <a href="#product-surfaces">Product surfaces</a> ·
  <a href="#specialized-ai-agents">AI Agents</a> ·
  <a href="#architecture">Architecture</a> ·
  <a href="#public-api-and-gaql">API & GAQL</a> ·
  <a href="#run-locally">Quick start</a> ·
  <a href="LICENSE">License</a>
</p>

</div>

---

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                ADSIQ SYSTEM ARCHITECTURE                                │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │                            NEXT.JS 14 FRONTEND (Port 3000)                        │  │
│  │   Control Center │ API Troubleshooter │ Campaign Builder │ Analytics │ Code       │  │
│  └─────────────────────────────────────────┬─────────────────────────────────────────┘  │
│                                            │ REST API + WebSockets                      │
│  ┌─────────────────────────────────────────▼─────────────────────────────────────────┐  │
│  │                            FASTAPI BACKEND (Port 8000)                            │  │
│  │   /api/v1/campaigns │ /api/v1/troubleshoot │ /api/v1/agents │ /ws/agents           │  │
│  └──────────────────┬───────────────────────────────────────┬────────────────────────┘  │
│                     │                                       │                           │
│  ┌──────────────────▼──────────────────┐         ┌──────────▼──────────┐                │
│  │      LANGGRAPH AGENT ENGINE         │         │     DATABASES       │                │
│  │  ─────────────────────────          │         │  PostgreSQL 16      │                │
│  │  🔧 Troubleshooter Agent            │         │  (Campaigns & Runs) │                │
│  │  🏗️ Campaign Builder Agent          │         │  Redis 7            │                │
│  │  🎨 Creative Agent                  │         │  (PubSub & Cache)   │                │
│  │  📊 Analytics GAQL Agent            │         └─────────────────────┘                │
│  │  💬 Solutions Consultant Agent      │                                                │
│  └─────────────────────────────────────┘                                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## Product film

[![Play the AdsIQ product film](docs/images/adsiq-product-launch-poster.png)](https://github.com/manasasb2000/AdsIQ)

**[▶ Play the AdsIQ Product Demo Video](https://github.com/manasasb2000/AdsIQ)**

---

## Product workflow

Six recorded operational views showing how **AdsIQ** transforms complex Google Ads API tasks into governed, reproducible developer and agent workflows:

<table>
  <tr>
    <td width="50%">
      <strong>01 · API Error Diagnosis & Fix Generation</strong><br>
      <a href="docs/images/01-troubleshooter.png"><img src="docs/images/01-troubleshooter.png" alt="AdsIQ API Troubleshooter showing root cause, request_id, and Python/Node code fix" width="100%"></a><br>
      <sub>Select from 50+ real Google Ads API error codes or paste raw <code>GoogleAdsFailure</code> logs to generate multi-language code fixes.</sub>
    </td>
    <td width="50%">
      <strong>02 · Natural Language Campaign Hierarchy Construction</strong><br>
      <a href="docs/images/02-campaign-builder.png"><img src="docs/images/02-campaign-builder.png" alt="AdsIQ AI Campaign Builder generating Account, Campaign, AdGroup, and Keywords" width="100%"></a><br>
      <sub>Convert business briefs into complete Google Ads entity hierarchies (Customer → Campaign → AdGroup → Keywords → RSA Ads).</sub>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <strong>03 · Responsive Search Ad (RSA) Copy & Policy Compliance</strong><br>
      <a href="docs/images/03-creative-studio.png"><img src="docs/images/03-creative-studio.png" alt="AdsIQ Creative Studio displaying 15 headlines and 4 descriptions with character counters" width="100%"></a><br>
      <sub>Generate 15 headlines (≤30 chars) and 4 descriptions (≤90 chars) with character limits and policy compliance checks.</sub>
    </td>
    <td width="50%">
      <strong>04 · GAQL Query Parsing & Performance Analytics</strong><br>
      <a href="docs/images/04-gaql-analytics.png"><img src="docs/images/04-gaql-analytics.png" alt="AdsIQ GAQL Analytics Console displaying query execution and row results" width="100%"></a><br>
      <sub>Execute raw Google Ads Query Language (GAQL) statements against simulated reporting datasets to analyze ROAS and CTR.</sub>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <strong>05 · Multi-Language SDK Code Playground</strong><br>
      <a href="docs/images/05-code-playground.png"><img src="docs/images/05-code-playground.png" alt="AdsIQ Code Playground generating Python and Node.js Google Ads SDK snippets" width="100%"></a><br>
      <sub>Generate executable client library snippets across Python SDK, Node.js Client, Java, and PHP.</sub>
    </td>
    <td width="50%">
      <strong>06 · Real-Time Agent Streaming & Thought Feed</strong><br>
      <a href="docs/images/06-agent-stream.png"><img src="docs/images/06-agent-stream.png" alt="AdsIQ Live Agent Feed streaming execution steps over WebSockets" width="100%"></a><br>
      <sub>Stream LangGraph state machine node transitions and thinking steps live over WebSockets to the Next.js control center.</sub>
    </td>
  </tr>
</table>

AdsIQ is an operational control plane built to simulate and automate the day-to-day responsibilities of a **Google Product Solutions Engineer (Ads API)**. It connects client-side developer requirements with server-side ad platform governance, providing structured troubleshooting, campaign creation, and performance reporting.

---

## Product surfaces

- `/` — **Main Control Center Dashboard**: KPI stat cards (Total Spend, ROAS, Quality Score, Active Campaigns), Recharts performance trend lines, and live WebSocket agent feed.
- `/troubleshoot` — **API Troubleshooter**: Interactive error diagnosis tool for 50+ real Google Ads API error codes, `request_id` inspection, and multi-language code fixes.
- `/campaigns` — **Campaign Manager**: Account hierarchy tree viewer (Customer → Campaign → AdGroup → Keywords → Ads).
- `/campaigns/new` — **AI Campaign Builder**: Converts natural language prompts into full campaign hierarchies and executable Python SDK code.
- `/creative` — **Creative Studio**: Generates Responsive Search Ad (RSA) copy with strict character counters (15 headlines ≤30 chars, 4 descriptions ≤90 chars).
- `/analytics` — **GAQL Query Console**: Execute raw Google Ads Query Language (GAQL) statements and inspect output rows.
- `/playground` — **API Code Playground**: Multi-language SDK code generator for Python, Node.js, Java, and PHP integration snippets.
- `/consultant` — **AI Solutions Consultant Chat**: Interactive technical advisor simulating partner technical support.

---

## Specialized AI Agents

AdsIQ uses a **LangGraph State Machine** to route tasks across 6 specialized AI agents:

| Agent | Icon | Role & Functionality |
|---|:---:|---|
| **Troubleshooter Agent** | 🔧 | Diagnoses Google Ads API errors, extracts `request_id`, generates code fixes in Python/Node/Java/PHP |
| **Campaign Builder Agent** | 🏗️ | Builds full account hierarchy (`Customer → Campaign → AdGroup → Keywords → RSA Ads`) from natural language briefs |
| **Creative Agent** | 🎨 | Generates 15 headlines (≤30 chars) and 4 descriptions (≤90 chars) compliant with Google Ads policies |
| **Analytics Agent** | 📊 | Parses GAQL statements, computes ROAS, CTR, Quality Score (1-10), and impression share metrics |
| **Solutions Consultant** | 💬 | Provides technical and architectural advice to external developers and advertisers |
| **Orchestrator Supervisor** | 🔄 | Manages graph state, evaluates prompt intent, and routes execution to target agent nodes |

---

## Architecture

### Frontend (Next.js 14 App Router)
- **Framework**: Next.js 14 + React 18 + TypeScript 5
- **Styling**: Dark Glassmorphism Design System with Tailwind CSS & CSS HSL variables
- **Data Fetching**: Axios REST client + Native WebSockets for real-time streaming
- **Visualization**: Recharts for performance trends & Lucide icons for UI components

### Backend (FastAPI + Python 3.12)
- **Framework**: FastAPI with async route handlers, CORS middleware, and GZip compression
- **ORM & DB**: SQLAlchemy 2.0 Async Engine + Asyncpg connection pooling + PostgreSQL 16
- **Cache & PubSub**: Redis 7 for caching and WebSocket broadcasting
- **Validation**: Pydantic v2 schemas for all HTTP request/response payloads

### AI & Agent Engine (LangGraph + LangChain)
- **Orchestration**: LangGraph state machine (`AgentState`) with stateful node transitions
- **Error Library**: 50+ built-in Google Ads API error codes, root cause analyses, and solutions
- **GAQL Engine**: In-memory GAQL query parser and reporting dataset runner

---

## Public API and GAQL

### REST API Endpoints

```http
POST   /api/v1/troubleshoot/      # Submit error code/log for AI diagnosis
GET    /api/v1/troubleshoot/library # List all 50+ supported error codes
POST   /api/v1/campaigns/         # Create campaign hierarchy
GET    /api/v1/campaigns/         # List all campaigns
POST   /api/v1/creative/generate  # Generate RSA headlines & descriptions
POST   /api/v1/analytics/gaql     # Execute GAQL query
GET    /api/v1/analytics/dashboard # Retrieve dashboard KPIs & chart series
POST   /api/v1/codegen/          # Generate multi-language SDK code
POST   /api/v1/agents/run        # Trigger LangGraph agent workflow
WS     /ws/agents                 # Stream live agent execution steps over WebSocket
```

### Sample GAQL Query

```sql
SELECT
    campaign.id,
    campaign.name,
    campaign.status,
    metrics.impressions,
    metrics.clicks,
    metrics.cost_micros,
    metrics.conversions,
    metrics.historical_quality_score
FROM campaign
WHERE campaign.status = 'ENABLED'
ORDER BY metrics.clicks DESC
```

---

## Run Locally

### Prerequisites
- [Docker](https://www.docker.com/) & Docker Compose
- Node.js 18+ & Python 3.12+ (if running outside Docker)

### Quick Start (Single Command with Docker)

```bash
# 1. Clone the repository
git clone https://github.com/manasasb2000/AdsIQ.git
cd AdsIQ

# 2. Copy environment template
cp .env.example .env

# 3. Start all services (PostgreSQL + Redis + FastAPI + Next.js)
docker compose up --build
```

Access the applications:
- **Frontend Control Center**: [http://localhost:3000](http://localhost:3000)
- **FastAPI REST API**: [http://localhost:8000](http://localhost:8000)
- **Interactive OpenAPI Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## License

Distributed under the MIT License. See [`LICENSE`](./LICENSE) for details.
