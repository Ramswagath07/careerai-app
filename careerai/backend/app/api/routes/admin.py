from fastapi import APIRouter, Depends
from app.core.security import get_admin_user
from app.core.database import get_db
from bson import ObjectId

router = APIRouter()

@router.get("/users")
async def list_users(skip: int = 0, limit: int = 50, admin=Depends(get_admin_user)):
    db = get_db()
    users = await db.users.find({}, {"password":0}).skip(skip).limit(limit).to_list(limit)
    for u in users:
        u["id"] = str(u.pop("_id"))
    return {"users": users, "total": await db.users.count_documents({})}

@router.delete("/users/{user_id}")
async def delete_user(user_id: str, admin=Depends(get_admin_user)):
    db = get_db()
    await db.users.delete_one({"_id": ObjectId(user_id)})
    await db.resumes.delete_many({"user_id": user_id})
    return {"message": "User deleted"}

@router.get("/stats")
async def admin_stats(admin=Depends(get_admin_user)):
    db = get_db()
    return {
        "total_users": await db.users.count_documents({}),
        "total_resumes": await db.resumes.count_documents({}),
        "pro_users": await db.users.count_documents({"plan":"pro"}),
    }
