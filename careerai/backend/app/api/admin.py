from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
from app.api.auth import get_current_user

router = APIRouter()

async def require_admin(user=Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(403, "Admin access required")
    return user

@router.get("/stats")
async def admin_stats(admin=Depends(require_admin), db=Depends(get_db)):
    users = await db.users.count_documents({})
    resumes = await db.resumes.count_documents({})
    return {"total_users": users, "total_resumes": resumes}

@router.get("/users")
async def list_users(skip: int = 0, limit: int = 50, admin=Depends(require_admin), db=Depends(get_db)):
    cursor = db.users.find({}, {"hashed_password": 0}).skip(skip).limit(limit)
    users = []
    async for u in cursor:
        u["id"] = str(u["_id"]); del u["_id"]
        users.append(u)
    return users
