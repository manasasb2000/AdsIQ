# ============================================================
# backend/app/models/agent_run.py
# ============================================================
#
# 📖 WHAT IS THIS MODEL FOR?
# Every time an AI agent runs, we log it here.
# This is how we build the "Agent Activity Feed" in the UI,
# and how we demonstrate OBSERVABILITY — a critical FDE skill.
#
# This table answers questions like:
#   - Which agent ran? When? How long did it take?
#   - What was the input? What did it output?
#   - Did it succeed or fail? What error occurred?
#   - How many LLM tokens were used? (= how much did it cost?)
#
# 📖 FDE RELEVANCE:
# In a real Google PSE role, you'd need to audit AI decisions,
# debug failures, and track costs. This model enables all of that.
# ============================================================

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Float, DateTime, Text, JSON
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import enum

from app.core.database import Base


class AgentType(str, enum.Enum):
    """The 6 agents in our LangGraph system."""
    ORCHESTRATOR = "ORCHESTRATOR"
    TROUBLESHOOTER = "TROUBLESHOOTER"
    CAMPAIGN_BUILDER = "CAMPAIGN_BUILDER"
    CREATIVE = "CREATIVE"
    ANALYTICS = "ANALYTICS"
    CONSULTANT = "CONSULTANT"


class AgentRunStatus(str, enum.Enum):
    PENDING = "PENDING"       # Queued but not started
    RUNNING = "RUNNING"       # Currently executing
    COMPLETED = "COMPLETED"   # Finished successfully
    FAILED = "FAILED"         # Finished with an error
    CANCELLED = "CANCELLED"   # Manually stopped


class AgentRun(Base):
    """
    Logs every AI agent execution for observability and debugging.
    Think of this as a flight recorder for AI agents.
    """
    __tablename__ = "agent_runs"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    agent_type: Mapped[AgentType] = mapped_column(SAEnum(AgentType), index=True)
    status: Mapped[AgentRunStatus] = mapped_column(
        SAEnum(AgentRunStatus), default=AgentRunStatus.PENDING, index=True
    )

    # What was sent TO the agent
    input_data: Mapped[Optional[dict]] = mapped_column(JSON)

    # What the agent produced
    output_data: Mapped[Optional[dict]] = mapped_column(JSON)

    # If it failed, what was the error?
    error_message: Mapped[Optional[str]] = mapped_column(Text)

    # LLM usage tracking (cost control)
    tokens_used: Mapped[int] = mapped_column(Integer, default=0)
    # Estimated cost in USD cents (e.g., 42 = $0.42)
    estimated_cost_cents: Mapped[float] = mapped_column(Float, default=0.0)

    # Performance tracking
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    # Duration in milliseconds
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer)

    # LangSmith trace ID — links to full trace in LangSmith dashboard
    langsmith_trace_id: Mapped[Optional[str]] = mapped_column(String(255))

    # Which campaign this run is related to (optional)
    campaign_id: Mapped[Optional[str]] = mapped_column(String(36))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AgentLog(Base):
    """
    Step-by-step logs within an agent run.
    Like console.log() statements but persisted to the database.
    Each row = one "thinking step" of the agent.
    """
    __tablename__ = "agent_logs"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4())
    )

    # Which agent run does this log belong to?
    run_id: Mapped[str] = mapped_column(String(36), index=True)

    # Name of the LangGraph node that produced this log
    # e.g., "research_tool", "generate_copy", "validate_output"
    step_name: Mapped[str] = mapped_column(String(100))

    # Human-readable log message
    message: Mapped[str] = mapped_column(Text)

    # Structured metadata (JSON) for any extra context
    metadata: Mapped[Optional[dict]] = mapped_column(JSON)

    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
