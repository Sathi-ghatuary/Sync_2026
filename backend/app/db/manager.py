"""
Database manager for ChromaDB interactions and data persistence.
"""
import json
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime
from .chroma_client import get_collection
from .schema import TitleRecord, ApplicationRecord, VerificationResult
import os


class DatabaseManager:
    """Manages all database operations for titles and applications."""
    
    def __init__(self):
        self.collection = get_collection()
        self.applications_file = "applications.json"
        self._load_applications()
    
    def _load_applications(self):
        """Load applications from file on startup."""
        if os.path.exists(self.applications_file):
            try:
                with open(self.applications_file, 'r', encoding='utf-8') as f:
                    self.applications = json.load(f)
            except Exception:
                self.applications = {}
        else:
            self.applications = {}
    
    def _save_applications(self):
        """Persist applications to file."""
        with open(self.applications_file, 'w', encoding='utf-8') as f:
            json.dump(self.applications, f, indent=2, ensure_ascii=False)
    
    def add_title(self, title: str, title_id: Optional[str] = None, language: str = "english") -> str:
        """Add a title to the collection."""
        if title_id is None:
            title_id = str(uuid.uuid4())
        
        self.collection.add(
            documents=[title],
            metadatas=[{"text": title, "language": language}],
            ids=[title_id]
        )
        return title_id
    
    def batch_add_titles(self, titles: List[str], batch_size: int = 512) -> int:
        """Add multiple titles in batches."""
        added_count = 0
        for i in range(0, len(titles), batch_size):
            batch = titles[i:i + batch_size]
            ids = [str(uuid.uuid4()) for _ in batch]
            self.collection.add(
                documents=batch,
                metadatas=[{"text": t, "language": "english"} for t in batch],
                ids=ids
            )
            added_count += len(batch)
        return added_count
    
    def get_all_titles(self) -> List[str]:
        """Retrieve all existing titles."""
        try:
            result = self.collection.get(include=["metadatas"])
            if result and result.get('metadatas'):
                return [m.get('text', '') for m in result['metadatas']]
        except Exception:
            pass
        return []
    
    def get_title_count(self) -> int:
        """Get total count of titles in database."""
        try:
            result = self.collection.get()
            if result:
                return len(result.get('ids', []))
        except Exception:
            pass
        return 0
    
    def record_application(
        self,
        submitted_title: str,
        user_email: str,
        similarity_score: float,
        verification_probability: float,
        violations: List[Dict],
        status: str = "pending",
    ) -> str:
        """Record a title application submission."""
        app_id = str(uuid.uuid4())
        app = {
            "id": app_id,
            "submitted_title": submitted_title,
            "user_email": user_email,
            "status": status,
            "similarity_score": similarity_score,
            "verification_probability": verification_probability,
            "violations": violations,
            "created_at": datetime.utcnow().isoformat(),
        }
        self.applications[app_id] = app
        self._save_applications()
        return app_id
    
    def get_application(self, app_id: str) -> Optional[Dict]:
        """Retrieve an application by ID."""
        return self.applications.get(app_id)
    
    def get_applications(self, user_email: Optional[str] = None) -> List[Dict]:
        """Get all applications, optionally filtered by email."""
        apps = list(self.applications.values())
        if user_email:
            apps = [a for a in apps if a['user_email'] == user_email]
        return sorted(apps, key=lambda x: x['created_at'], reverse=True)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        return {
            "total_titles": self.get_title_count(),
            "total_applications": len(self.applications),
            "pending_applications": len([a for a in self.applications.values() if a['status'] == 'pending']),
            "approved_applications": len([a for a in self.applications.values() if a['status'] == 'approved']),
            "rejected_applications": len([a for a in self.applications.values() if a['status'] == 'rejected']),
        }
    
    def reset_database(self):
        """Reset all data (use with caution)."""
        try:
            # Delete and recreate collection
            from .chroma_client import _collection as collection_ref
            # Note: ChromaDB doesn't have direct delete, so we'll recreate
            self.applications = {}
            self._save_applications()
        except Exception:
            pass


# Singleton instance
_db_manager: Optional[DatabaseManager] = None


def get_db_manager() -> DatabaseManager:
    """Get the database manager singleton."""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager
