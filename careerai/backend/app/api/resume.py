"""Resume upload, analysis, and retrieval API routes"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from bson import ObjectId
from datetime import datetime
import os, uuid, logging

from app.core.database import get_db
from app.core.config import settings
from app.api.auth import get_current_user
from app.ml.text_extractor import extract_text, count_pages
from app.ml.ats_scorer import ats_scorer
from app.ml.career_recommender import recommend_careers

router = APIRouter()
logger = logging.getLogger(__name__)

MAX_BYTES = settings.MAX_FILE_SIZE_MB * 1024 * 1024

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...), user=Depends(get_current_user), db=Depends(get_db)):
    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"File type '{ext}' not supported. Use: {', '.join(settings.ALLOWED_EXTENSIONS)}")

    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(413, f"File too large. Max {settings.MAX_FILE_SIZE_MB} MB.")

    # Save file
    uid = str(uuid.uuid4())
    save_name = f"{uid}.{ext}"
    save_path = os.path.join(settings.UPLOAD_DIR, save_name)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(data)

    # Extract + analyze
    text = extract_text(data, file.filename)
    pages = count_pages(data, file.filename)
    analysis = ats_scorer.score(text)
    analysis["page_count"] = pages
    analysis["extracted_text"] = text[:5000]  # truncate for storage

    careers = recommend_careers(analysis.get("detected_skills", []))

    doc = {
        "user_id": str(user["_id"]),
        "filename": file.filename,
        "file_path": save_path,
        "file_size": len(data),
        "file_type": ext,
        "analysis": analysis,
        "career_matches": careers,
        "created_at": datetime.utcnow(),
    }
    result = await db.resumes.insert_one(doc)
    await db.users.update_one({"_id": user["_id"]}, {"$inc": {"resume_count": 1}})

    return {
        "id": str(result.inserted_id),
        "filename": file.filename,
        "file_size": len(data),
        "analysis": analysis,
        "career_matches": careers,
    }

@router.get("/history")
async def resume_history(user=Depends(get_current_user), db=Depends(get_db)):
    cursor = db.resumes.find({"user_id": str(user["_id"])}).sort("created_at", -1).limit(20)
    resumes = []
    async for r in cursor:
        r["id"] = str(r["_id"]); del r["_id"]
        r.pop("analysis", {}).pop("extracted_text", None)
        resumes.append(r)
    return resumes

@router.get("/{resume_id}")
async def get_resume(resume_id: str, user=Depends(get_current_user), db=Depends(get_db)):
    r = await db.resumes.find_one({"_id": ObjectId(resume_id), "user_id": str(user["_id"])})
    if not r:
        raise HTTPException(404, "Resume not found")
    r["id"] = str(r["_id"]); del r["_id"]
    return r

@router.delete("/{resume_id}")
async def delete_resume(resume_id: str, user=Depends(get_current_user), db=Depends(get_db)):
    r = await db.resumes.find_one({"_id": ObjectId(resume_id), "user_id": str(user["_id"])})
    if not r:
        raise HTTPException(404, "Resume not found")
    if os.path.exists(r.get("file_path", "")):
        os.remove(r["file_path"])
    await db.resumes.delete_one({"_id": ObjectId(resume_id)})
    await db.users.update_one({"_id": user["_id"]}, {"$inc": {"resume_count": -1}})
    return {"message": "Resume deleted"}
