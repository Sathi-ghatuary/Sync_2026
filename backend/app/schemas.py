from pydantic import BaseModel
from typing import List, Optional


class TitleRequest(BaseModel):
    title: str


class RuleViolation(BaseModel):
    rule: str
    message: str


class TitleResponse(BaseModel):
    title: str
    similarity_score: float
    verification_probability: float
    violations: List[RuleViolation] = []
    similar_titles: List[str] = []


class ApplicationRequest(BaseModel):
    title: str
    user_email: str


class ApplicationResponse(BaseModel):
    application_id: str
    title: str
    status: str
    similarity_score: float
    verification_probability: float
    violations: List[RuleViolation] = []
    similar_titles: List[str] = []


class DatabaseStats(BaseModel):
    total_titles: int
    total_applications: int
    pending_applications: int
    approved_applications: int
    rejected_applications: int


class BulkIngestRequest(BaseModel):
    titles: List[str]
