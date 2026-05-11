from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from bson import ObjectId
from app.models.user import UserRegister, UserLogin, TokenResponse, UserResponse
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, get_current_user
from app.core.database import get_db

router = APIRouter()

def serialize_user(user: dict) -> UserResponse:
    return UserResponse(
        id=str(user["_id"]),
        name=user["name"],
        email=user["email"],
        role=user.get("role", "user"),
        plan=user.get("plan", "free"),
        resume_count=user.get("resume_count", 0),
        created_at=user.get("created_at", datetime.utcnow()),
        target_role=user.get("target_role"),
        location=user.get("location"),
    )

@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(data: UserRegister):
    db = get_db()
    if await db.users.find_one({"email": data.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_doc = {
        "name": data.name,
        "email": data.email,
        "password": hash_password(data.password),
        "role": "user",
        "plan": "free",
        "resume_count": 0,
        "created_at": datetime.utcnow(),
        "is_active": True,
    }
    result = await db.users.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    
    token_data = {"sub": str(result.inserted_id)}
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
        user=serialize_user(user_doc),
    )

@router.post("/login", response_model=TokenResponse)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    db = get_db()
    user = await db.users.find_one({"email": form.username})
    if not user or not verify_password(form.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not user.get("is_active", True):
        raise HTTPException(status_code=403, detail="Account deactivated")
    
    token_data = {"sub": str(user["_id"])}
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
        user=serialize_user(user),
    )

@router.get("/me", response_model=UserResponse)
async def get_me(current_user=Depends(get_current_user)):
    return serialize_user(current_user)

@router.put("/me")
async def update_profile(data: dict, current_user=Depends(get_current_user)):
    db = get_db()
    allowed = {k: v for k, v in data.items() if k in ("name","target_role","location","experience_level")}
    await db.users.update_one({"_id": current_user["_id"]}, {"$set": allowed})
    updated = await db.users.find_one({"_id": current_user["_id"]})
    return serialize_user(updated)
