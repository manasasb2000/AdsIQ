# ============================================================
# backend/app/schemas/agent.py
# ============================================================

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.models.agent_run import AgentType, AgentRunStatus

class AgentRunRequest(BaseModel):
    agent_type: AgentType = Field(..., description="Which agent to run")
    prompt: str = Field(..., description="User prompt / directive for the agent")
    campaign_id: Optional[str] = Field(None, description="Associated campaign ID if applicable")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Extra state / metadata for the agent graph")

class AgentLogSchema(BaseModel):
    id: str
    run_id: str
    step_name: str
    message: str
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime

class AgentRunResponse(BaseModel):
    id: str
    agent_type: AgentType
    status: AgentRunStatus
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    tokens_used: int = 0
    estimated_cost_cents: float = 0.0
    duration_ms: Optional[int] = None
    created_at: datetime
    logs: List[AgentLogSchema] = []
