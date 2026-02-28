from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from .schemas import (
    TitleRequest,
    TitleResponse,
    RuleViolation,
    ApplicationRequest,
    ApplicationResponse,
    DatabaseStats,
    BulkIngestRequest,
)
from .services.verifier import TitleVerifier
from .db.manager import get_db_manager
from .config import settings
import csv
import io

app = FastAPI(
    title="Title Verification API",
    description="PRGI Title Verification & Compliance System",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

verifier = TitleVerifier()
db_manager = get_db_manager()


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "message": "Title Verification API is running"}


@app.post("/verify", response_model=TitleResponse)
def verify_title(request: TitleRequest):
    """
    Verify a new title for compliance and similarity.
    
    Returns:
    - similarity_score: 0-1, probability this title is similar to existing ones
    - verification_probability: 0-1, probability title will be approved
    - violations: List of rule violations if any
    - similar_titles: List of existing titles that are similar
    """
    if not request.title or request.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title must be non-empty")
    
    result = verifier.verify(request.title)
    return TitleResponse(
        title=request.title,
        similarity_score=result["similarity_score"],
        verification_probability=result["verification_probability"],
        violations=result["violations"],
        similar_titles=result["similar_titles"],
    )


@app.post("/application", response_model=ApplicationResponse)
def submit_application(request: ApplicationRequest):
    """
    Submit a title application with email tracking.
    """
    if not request.title or request.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title must be non-empty")
    if not request.user_email or request.user_email.strip() == "":
        raise HTTPException(status_code=400, detail="Email must be provided")
    
    result = verifier.verify(request.title)

    # Determine status based on violations and probability
    status = "approved" if result["verification_probability"] > settings.MIN_VERIFICATION_PROBABILITY_FOR_APPROVAL and not result["violations"] else "rejected"
    violations_payload = [v.model_dump() if hasattr(v, "model_dump") else v for v in result["violations"]]
    
    # Record the application
    app_id = db_manager.record_application(
        submitted_title=request.title,
        user_email=request.user_email,
        similarity_score=result["similarity_score"],
        verification_probability=result["verification_probability"],
        violations=violations_payload,
        status=status,
    )
    
    return ApplicationResponse(
        application_id=app_id,
        title=request.title,
        status=status,
        similarity_score=result["similarity_score"],
        verification_probability=result["verification_probability"],
        violations=result["violations"],
        similar_titles=result["similar_titles"],
    )


@app.get("/applications/{user_email}")
def get_user_applications(user_email: str):
    """Retrieve all applications submitted by a user."""
    apps = db_manager.get_applications(user_email=user_email)
    return {"user_email": user_email, "applications": apps}


@app.get("/database/stats", response_model=DatabaseStats)
def get_database_stats():
    """Get database statistics."""
    stats = db_manager.get_stats()
    return DatabaseStats(**stats)


@app.get("/database/titles/count")
def get_title_count():
    """Get total number of titles in database."""
    count = db_manager.get_title_count()
    return {"total_titles": count}


@app.post("/database/ingest/csv")
async def ingest_csv_file(file: UploadFile = File(...)):
    """
    Ingest titles from a CSV file.
    CSV should have one title per row. First column is used by default.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    try:
        contents = await file.read()
        stream = io.StringIO(contents.decode('utf-8-sig'))
        reader = csv.reader(stream)
        
        titles = []
        for row in reader:
            if row and row[0].strip():
                titles.append(row[0].strip())
        
        if not titles:
            raise HTTPException(status_code=400, detail="No valid titles found in CSV")
        
        count = db_manager.batch_add_titles(titles)
        verifier.invalidate_cache()
        stats = db_manager.get_stats()
        
        return {
            "message": f"Successfully ingested {count} titles",
            "count": count,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/database/ingest/bulk", response_model=dict)
def ingest_bulk_titles(request: BulkIngestRequest):
    """
    Ingest multiple titles at once via API.
    """
    if not request.titles:
        raise HTTPException(status_code=400, detail="Titles list must not be empty")
    
    count = db_manager.batch_add_titles(request.titles)
    verifier.invalidate_cache()
    stats = db_manager.get_stats()
    
    return {
        "message": f"Successfully ingested {count} titles",
        "count": count,
        "stats": stats
    }


@app.get("/database/reset")
def reset_database():
    """Reset database (WARNING: This deletes all data)."""
    db_manager.reset_database()
    verifier.invalidate_cache()
    return {"message": "Database reset successfully"}

@app.post("/conflict-timeline")
def get_conflict_timeline(request: TitleRequest):
    """
    Returns conflict ancestry chain for a given title.
    Shows: root registered title → similar rejected applications → new title position
    """
    if not request.title or request.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title must be non-empty")

    title = request.title.strip()

    # Step 1: Get similar titles from ChromaDB
    try:
        query_res = verifier.collection.query(
            query_texts=[title],
            n_results=5,
        )
    except Exception:
        return {"title": title, "conflict_chain": [], "rejected_siblings": [], "root_title": None}

    if not query_res or not query_res.get("documents") or not query_res["documents"][0]:
        return {"title": title, "conflict_chain": [], "rejected_siblings": [], "root_title": None}

    similar_docs = query_res["documents"][0]
    distances = query_res["distances"][0]
    similarities = [round((1 - d) * 100, 1) for d in distances]

    # Step 2: Find rejected applications that are similar to the same root titles
    all_applications = list(db_manager.applications.values())
    rejected_apps = [a for a in all_applications if a["status"] == "rejected"]

    # Step 3: Build conflict chain
    conflict_chain = []
    for i, existing_title in enumerate(similar_docs):
        if existing_title.lower() == title.lower():
            continue
        sim = similarities[i] if i < len(similarities) else 0

        # Find rejected applications similar to this existing title
        related_rejections = []
        for app in rejected_apps:
            app_title = app.get("submitted_title", "")
            if app_title.lower() == title.lower():
                continue
            # Check if this rejected app was similar to the same root
            app_violations = app.get("violations", [])
            for v in app_violations:
                msg = v.get("message", "") if isinstance(v, dict) else str(v)
                if existing_title.lower() in msg.lower():
                    related_rejections.append({
                        "title": app_title,
                        "rejected_at": app.get("created_at", ""),
                        "similarity_score": round(app.get("similarity_score", 0) * 100, 1),
                        "reason": msg[:80] + "..." if len(msg) > 80 else msg,
                    })
                    break

        conflict_chain.append({
            "root_title": existing_title,
            "similarity_to_new": sim,
            "related_rejections": related_rejections[:3],
        })

    # Step 4: Find root (highest similarity match)
    root_title = similar_docs[0] if similar_docs else None
    root_similarity = similarities[0] if similarities else 0

    # Step 5: Count total conflict family size
    total_rejected_in_family = sum(len(c["related_rejections"]) for c in conflict_chain)

    return {
        "title": title,
        "root_title": root_title,
        "root_similarity": root_similarity,
        "conflict_chain": conflict_chain[:3],
        "total_rejected_in_family": total_rejected_in_family,
        "summary": (
            f"'{title}' conflicts with root title '{root_title}' ({root_similarity}% similar). "
            f"{total_rejected_in_family} previously rejected titles share the same conflict ancestry."
            if root_title else "No significant conflicts found."
        )
    }

