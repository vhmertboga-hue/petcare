import os
import json
from typing import Optional, Dict, Any
import httpx
from backend.app.models.ai_request_log import AIRequestLog
from sqlalchemy.ext.asyncio import AsyncSession

DEFAULT_DAILY_LIMIT = int(os.getenv("AI_DAILY_LIMIT", "10"))


async def check_and_log_usage(db: AsyncSession, user_id: Optional[int]) -> bool:
    # simple count of requests today
    from datetime import date, datetime
    start = datetime.combine(date.today(), datetime.min.time())
    q = await db.execute("SELECT COUNT(1) FROM ai_request_logs WHERE user_id = :uid AND created_at >= :start", {"uid": user_id, "start": start})
    count = q.scalar() or 0
    return count < DEFAULT_DAILY_LIMIT


async def call_ai_and_log(db: AsyncSession, user_id: Optional[int], payload: Dict[str, Any]) -> Dict[str, Any]:
    """Call external AI provider (if configured). Log request and response in AIRequestLog.
    If no API key provided, return a safe mock response with status 'mock'."""
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("AI_API_KEY")
    prompt = json.dumps(payload)
    log = AIRequestLog(user_id=user_id, species=payload.get("species"), prompt=prompt)
    db.add(log)
    await db.flush()

    if not api_key:
        # return mock, do not pretend to be accurate
        response = {
            "possible_causes": [{"cause": "Infection (mock)", "confidence": "low", "notes": "No API key configured."}],
            "severity": "unknown",
            "needs_vet": True,
            "urgent_signs": ["severe bleeding","collapse"],
            "general_care": ["Keep animal warm","Avoid feeding until vet advises"],
            "disclaimer": "This is a mock response because no AI key is configured. Visit a vet for diagnosis."
        }
        log.response = json.dumps(response)
        log.status = "mock"
        await db.commit()
        return response

    # build a safe prompt for the model
    system = "You are an assistant that suggests possible veterinary causes and advice. Always include disclaimer and urgent signs. Do not provide definitive diagnosis."
    user_text = f"Species: {payload.get('species')}\nBreed: {payload.get('breed')}\nAge: {payload.get('age')}\nGender: {payload.get('gender')}\nWeight: {payload.get('weight')}\nSymptom: {payload.get('symptom')}\nDuration (days): {payload.get('symptom_duration_days')}\nBehavior change: {payload.get('behavior_change')}"

    # call OpenAI Chat Completions (example), use httpx
    try:
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        body = {
            "model": "gpt-4o-mini",  # placeholder
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user_text}
            ],
            "max_tokens": 400,
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body)
            resp.raise_for_status()
            data = resp.json()
        # Parse response naively into structured fields — expect model to return JSON-like text.
        content = data.get("choices", [])[0].get("message", {}).get("content", "")
        result = {"raw": content}
        log.response = content
        log.status = "success"
        # tokens and cost extraction if available
        usage = data.get("usage")
        if usage:
            log.tokens_used = usage.get("total_tokens")
        await db.commit()
        return result
    except Exception as e:
        log.status = "error"
        log.error = str(e)
        await db.commit()
        return {"error": "AI provider error", "details": str(e)}
