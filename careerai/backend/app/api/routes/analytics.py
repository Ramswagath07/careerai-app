from fastapi import APIRouter, Depends
from app.core.security import get_current_user, get_admin_user
from app.core.database import get_db

router = APIRouter()

@router.get("/dashboard")
async def user_analytics(current_user=Depends(get_current_user)):
    db = get_db()
    uid = str(current_user["_id"])
    resumes = await db.resumes.find({"user_id": uid}, {"analysis.ats_score":1,"created_at":1}).sort("created_at",-1).to_list(10)
    scores = [r["analysis"]["ats_score"] for r in resumes if "analysis" in r]
    return {
        "resume_count": current_user.get("resume_count", 0),
        "avg_ats_score": round(sum(scores)/len(scores)) if scores else 0,
        "best_score": max(scores) if scores else 0,
        "score_trend": scores[::-1],
        "career_matches_count": 6,
    }

@router.get("/market")
async def market_trends():
    return {
        "job_openings": {"Software Engineer":48230,"Data Analyst":23100,"AI/ML Engineer":18750,"Cloud Engineer":31200,"Cybersecurity":22400},
        "salary_ranges": {"Software Engineer":"$85K–$140K","Data Analyst":"$65K–$100K","AI/ML Engineer":"$110K–$165K","Cloud Engineer":"$95K–$145K"},
        "monthly_demand": [42,45,44,50,55,58,62,65,68,72,70,75],
        "top_skills_2025": ["Python","TypeScript","Kubernetes","LLM/GenAI","Rust","dbt","Terraform"],
        "remote_percentage": 67,
        "yoy_growth": 23,
    }

@router.get("/admin/overview")
async def admin_overview(admin=Depends(get_admin_user)):
    db = get_db()
    total_users = await db.users.count_documents({})
    total_resumes = await db.resumes.count_documents({})
    return {"total_users": total_users, "total_resumes": total_resumes, "active_today": 12}
