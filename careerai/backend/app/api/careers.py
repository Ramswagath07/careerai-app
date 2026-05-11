from fastapi import APIRouter, Depends
from app.api.auth import get_current_user
from app.ml.career_recommender import CAREERS_DB, recommend_careers

router = APIRouter()

@router.get("/")
async def list_careers():
    return CAREERS_DB

@router.get("/recommend")
async def get_recommendations(skills: str = "", user=Depends(get_current_user)):
    skill_list = [s.strip() for s in skills.split(",") if s.strip()]
    return recommend_careers(skill_list)
