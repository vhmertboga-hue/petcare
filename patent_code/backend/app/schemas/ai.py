from pydantic import BaseModel
from typing import Optional, List


class AIDiagnoseRequest(BaseModel):
    species: str
    breed: Optional[str]
    age: Optional[str]
    gender: Optional[str]
    weight: Optional[float]
    symptom: str
    symptom_duration_days: Optional[int]
    behavior_change: Optional[str]
    photo_file_id: Optional[int]


class AIPossibleCause(BaseModel):
    cause: str
    confidence: Optional[str]
    notes: Optional[str]


class AIDiagnoseResponse(BaseModel):
    possible_causes: List[AIPossibleCause]
    severity: str
    needs_vet: bool
    urgent_signs: List[str]
    general_care: List[str]
    disclaimer: str
