from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.api.auth import get_current_user

router = APIRouter()

@router.get("/dashboard")
async def dashboard_analytics(user=Depends(get_current_user), db=Depends(get_db)):
    uid = str(user["_id"])
    total = await db.resumes.count_documents({"user_id": uid})
    pipeline = [
        {"$match": {"user_id": uid}},
        {"$group": {"_id": None, "avg_ats": {"$avg": "$analysis.ats_score"}, "max_ats": {"$max": "$analysis.ats_score"}}},
    ]
    agg = await db.resumes.aggregate(pipeline).to_list(1)
    stats = agg[0] if agg else {"avg_ats": 0, "max_ats": 0}
    return {
        "total_resumes": total,
        "avg_ats_score": round(stats.get("avg_ats") or 0, 1),
        "best_ats_score": round(stats.get("max_ats") or 0, 1),
        "job_market_trends": _market_trends(),
        "salary_by_role": _salary_data(),
    }

def _market_trends():
    return {
        "labels": ["Jun","Jul","Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May"],
        "software_eng": [42,45,44,50,55,58,62,65,68,72,70,75],
        "ai_ml": [30,33,36,40,45,50,55,58,62,68,72,78],
        "cloud": [35,36,38,42,44,46,50,53,55,58,60,63],
    }

def _salary_data():
    return [
        {"role": "SWE", "avg_salary": 112},
        {"role": "ML Eng", "avg_salary": 135},
        {"role": "Cloud", "avg_salary": 118},
        {"role": "Data Analyst", "avg_salary": 88},
        {"role": "UI/UX", "avg_salary": 92},
        {"role": "Security", "avg_salary": 105},
    ]
