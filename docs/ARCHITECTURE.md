# 🏗️ AdsIQ System Architecture

## Overview
AdsIQ is an enterprise-grade, multi-agent AI platform built specifically for Google Ads API integration, campaign hierarchy generation, and error troubleshooting.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       NEXT.JS 14 FRONTEND (App Router)                   │
│  Control Center │ API Troubleshooter │ Campaign Builder │ Analytics │ Code │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ REST API + WebSockets
┌────────────────────────────────────▼────────────────────────────────────┐
│                        FASTAPI BACKEND (Python 3.12)                     │
│  /api/v1/campaigns │ /api/v1/troubleshoot │ /api/v1/agents │ /ws/agents│
└──────────────────┬─────────────────────────────────────┬────────────────┘
                   │                                     │
┌──────────────────▼──────────────────┐       ┌──────────▼──────────┐
│      LANGGRAPH AGENT ENGINE         │       │  DATA STORAGE       │
│  ─────────────────────────          │       │  PostgreSQL 16      │
│  🔧 Troubleshooter Node             │       │  (Campaigns, Runs)  │
│  🏗️ Campaign Builder Node            │       │  Redis 7            │
│  🎨 Creative Agent Node             │       │  (PubSub & Cache)   │
│  📊 Analytics GAQL Node             │       └─────────────────────┘
│  💬 Solutions Consultant Node       │
└─────────────────────────────────────┘
```

## Core Systems

### 1. LangGraph Multi-Agent Engine
The agent system uses a state machine graph where `AgentState` passes typed context between nodes.
- **Troubleshooter Node**: Inspects error codes, parses `GoogleAdsFailure` details, generates multi-language fixes.
- **Campaign Builder Node**: Takes natural language briefs and creates complete Google Ads hierarchies (Customer → Campaign → AdGroup → Keywords → RSA Ads).
- **Creative Node**: Generates RSA headlines (max 30 chars) and descriptions (max 90 chars) with policy validation.
- **Analytics Node**: Executes GAQL statements and computes ROAS / Quality Score diagnostics.
- **Consultant Node**: Provides technical advice formatted for Google Ads partners.

### 2. GAQL Engine
Parses and executes Google Ads Query Language statements against campaign data.

### 3. Real-Time Streaming
FastAPI WebSockets broadcast agent thinking steps live to the Next.js control center.
