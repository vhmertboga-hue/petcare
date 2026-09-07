from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.session import get_db
from backend.app.api.api_v1.dependencies import get_current_user
from backend.app.schemas.ai import AIDiagnoseRequest, AIDiagnoseResponse
from backend.app.services.ai_service import check_and_log_usage, call_ai_and_log

router = APIRouter()


@router.post("/ai/diagnose", response_model=AIDiagnoseResponse)
async def diagnose(payload: AIDiagnoseRequest, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    # rate limit
    allowed = await check_and_log_usage(db, current_user.id)
    if not allowed:
        raise HTTPException(status_code=429, detail="Daily AI request limit reached")

    # call AI and log
    result = await call_ai_and_log(db, current_user.id, payload.dict())
    if result.get("error"):
        # return structured safe response with error note
        return AIDiagnoseResponse(
            possible_causes=[{"cause": "Unavailable (AI error)", "confidence": "unknown", "notes": "AI service error"}],
            severity="unknown",
            needs_vet=True,
            urgent_signs=["see admin logs"],
            general_care=["Please contact a veterinarian."],
            disclaimer="This information does not replace veterinary examination."
        )

    # if mock response returned (no API key), unify into AIDiagnoseResponse
    if result.get("possible_causes"):
        return AIDiagnoseResponse(**result)

    # fallback raw
    raw = result.get("raw") if isinstance(result, dict) else str(result)
    return AIDiagnoseResponse(
        possible_causes=[{"cause": raw, "confidence": "low", "notes": "Raw model output."}],
        severity="unknown",
        needs_vet=True,
        urgent_signs=[],
        general_care=[],
        disclaimer="This information does not replace veterinary examination."
    )
