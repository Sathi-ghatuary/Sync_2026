"""
Database schema and data models for title verification system.
"""
from datetime import datetime
from typing import List, Optional


class TitleRecord:
    """Represents a title in the database (existing registered titles)."""
    
    def __init__(self, title_id: str, title: str, language: str = "english", created_at: datetime = None):
        self.title_id = title_id
        self.title = title
        self.language = language
        self.created_at = created_at or datetime.utcnow()


class ApplicationRecord:
    """Represents a title application submission."""
    
    def __init__(
        self,
        application_id: str,
        submitted_title: str,
        user_email: str,
        status: str = "pending",  # pending, approved, rejected
        similarity_score: float = 0.0,
        verification_probability: float = 0.0,
        violations: Optional[List[dict]] = None,
        created_at: datetime = None,
    ):
        self.application_id = application_id
        self.submitted_title = submitted_title
        self.user_email = user_email
        self.status = status
        self.similarity_score = similarity_score
        self.verification_probability = verification_probability
        self.violations = violations or []
        self.created_at = created_at or datetime.utcnow()


class VerificationResult:
    """Result of title verification."""
    
    def __init__(
        self,
        title: str,
        similarity_score: float,
        verification_probability: float,
        violations: List[dict],
        similar_titles: Optional[List[str]] = None,
    ):
        self.title = title
        self.similarity_score = similarity_score
        self.verification_probability = verification_probability
        self.violations = violations
        self.similar_titles = similar_titles or []
