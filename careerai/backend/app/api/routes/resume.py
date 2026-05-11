from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from datetime import datetime
from bson import ObjectId
from app.core.security import get_current_user
from app.core.database import get_db
from app.core.config import settings
from app.ml.resume_analyzer import analyze_resume_full
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

MAX_BYTES = settings.MAX_FILE_SIZE_MB * 1024 * 1024

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...), current_user=Depends(get_current_user)):
    # Validate extension
    ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"File type .{ext} not allowed. Use PDF, DOCX, or TXT.")
    
    # Read and size-check
    content = await file.read()
    if len(content) > MAX_BYTES:
        raise HTTPException(status_code=413, detail=f"File too large. Max size: {settings.MAX_FILE_SIZE_MB}MB")
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="File is empty")
    
    # Analyze
    try:
        result = analyze_resume_full(content, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail="Resume analysis failed. Please try again.")
    
    db = get_db()
    
    # Save to DB
    resume_doc = {
        "user_id": str(current_user["_id"]),
        "filename": file.filename,
        "file_size": len(content),
        "analysis": {
            "ats_score": result["ats_score"],
            "keyword_score": result["keyword_score"],
            "contact_score": result["contact_score"],
            "experience_score": result["experience_score"],
            "education_score": result["education_score"],
            "skills_score": result["skills_score"],
            "format_score": result["format_score"],
            "detected_skills": result["detected_skills"],
            "missing_skills": result["missing_skills"],
            "experience_years": result["experience_years"],
            "education_level": result["education_level"],
            "certifications": result["certifications"],
            "word_count": result["word_count"],
            "recommendations": result["recommendations"],
            "extracted_text": result["extracted_text"],
        },
        "career_matches": result["career_matches"],
        "created_at": datetime.utcnow(),
    }
    
    ins = await db.resumes.insert_one(resume_doc)
    
    # Update user resume count
    await db.users.update_one(
        {"_id": current_user["_id"]},
        {"$inc": {"resume_count": 1}}
    )
    
    return {
        "id": str(ins.inserted_id),
        "filename": file.filename,
        "file_size": len(content),
        "ats_score": result["ats_score"],
        "keyword_score": result["keyword_score"],
        "contact_score": result["contact_score"],
        "experience_score": result["experience_score"],
        "education_score": result["education_score"],
        "skills_score": result["skills_score"],
        "format_score": result["format_score"],
        "detected_skills": result["detected_skills"],
        "missing_skills": result["missing_skills"],
        "experience_years": result["experience_years"],
        "education_level": result["education_level"],
        "certifications": result["certifications"],
        "word_count": result["word_count"],
        "recommendations": result["recommendations"],
        "extracted_text": result["extracted_text"],
        "career_matches": result["career_matches"],
        "created_at": datetime.utcnow().isoformat(),
    }

@router.get("/history")
async def get_resume_history(current_user=Depends(get_current_user)):
    db = get_db()
    resumes = await db.resumes.find(
        {"user_id": str(current_user["_id"])},
        {"analysis.extracted_text": 0}
    ).sort("created_at", -1).limit(20).to_list(length=20)
    for r in resumes:
        r["id"] = str(r.pop("_id"))
    return resumes

@router.get("/{resume_id}")
async def get_resume(resume_id: str, current_user=Depends(get_current_user)):
    db = get_db()
    try:
        oid = ObjectId(resume_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid resume ID")
    r = await db.resumes.find_one({"_id": oid, "user_id": str(current_user["_id"])})
    if not r:
        raise HTTPException(status_code=404, detail="Resume not found")
    r["id"] = str(r.pop("_id"))
    return r

@router.delete("/{resume_id}")
async def delete_resume(resume_id: str, current_user=Depends(get_current_user)):
    db = get_db()
    try:
        oid = ObjectId(resume_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid resume ID")
    result = await db.resumes.delete_one({"_id": oid, "user_id": str(current_user["_id"])})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Resume not found")
    await db.users.update_one({"_id": current_user["_id"]}, {"$inc": {"resume_count": -1}})
    return {"message": "Resume deleted"}
