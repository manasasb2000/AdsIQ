# ============================================================
# backend/app/api/v1/agents.py
# ============================================================

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.core.database import get_db
from app.schemas.agent import AgentRunRequest, AgentRunResponse
from app.models.agent_run import AgentRun, AgentLog, AgentRunStatus
from app.agents.graph import execute_agent_workflow

router = APIRouter()


@router.post("/run", response_model=AgentRunResponse)
async def run_agent(
    request: AgentRunRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Trigger an AI Agent Workflow (LangGraph State Machine).
    Executes Troubleshooter, CampaignBuilder, Creative, Analytics, or Consultant agent.
    """
    # 1. Execute agent graph
    result = await execute_agent_workflow(
        agent_type=request.agent_type.value,
        prompt=request.prompt,
        campaign_id=request.campaign_id
    )

    # 2. Persist run to Database
    db_run = AgentRun(
        agent_type=request.agent_type,
        status=AgentRunStatus.COMPLETED,
        input_data={"prompt": request.prompt, "context": request.context},
        output_data=result["results"],
        tokens_used=450,
        estimated_cost_cents=0.15,
        duration_ms=result["duration_ms"],
        campaign_id=request.campaign_id
    )
    db.add(db_run)
    await db.flush()

    # 3. Persist logs
    logs_output = []
    for log_entry in result["logs"]:
        db_log = AgentLog(
            run_id=db_run.id,
            step_name=log_entry["step_name"],
            message=log_entry["message"]
        )
        db.add(db_log)
        logs_output.append({
            "id": str(uuid.uuid4()),
            "run_id": db_run.id,
            "step_name": log_entry["step_name"],
            "message": log_entry["message"],
            "timestamp": db_run.created_at
        })

    await db.commit()
    await db.refresh(db_run)

    return AgentRunResponse(
        id=db_run.id,
        agent_type=db_run.agent_type,
        status=db_run.status,
        input_data=db_run.input_data,
        output_data=db_run.output_data,
        tokens_used=db_run.tokens_used,
        estimated_cost_cents=db_run.estimated_cost_cents,
        duration_ms=db_run.duration_ms,
        created_at=db_run.created_at,
        logs=logs_output
    )
