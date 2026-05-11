"""Authentication API routes — register, login, refresh, me"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime
from bson import ObjectId

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.models.user import UserCreate, UserLogin, UserInDB, UserPublic, TokenResponse

router = APIRouter()
bearer = HTTPBearer()

def _user_to_public(u: dict) -> UserPublic:
    u["id"] = str(u["_id"])
    return UserPublic(**u)

async def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer), db=Depends(get_db)):
    payload = decode_token(creds.credentials)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = await db.users.find_one({"_id": ObjectId(payload["sub"])})
    if not user or not user.get("is_active"):
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user

@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(data: UserCreate, db=Depends(get_db)):
    if await db.users.find_one({"email": data.email}):
        raise HTTPException(status_code=409, detail="Email already registered")
    user_doc = {
        "email": data.email,
        "full_name": data.full_name,
        "hashed_password": hash_password(data.password),
        "role": "user",
        "is_active": True,
        "plan": "free",
        "resume_count": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    result = await db.users.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    uid = str(result.inserted_id)
    access = create_access_token({"sub": uid})
    refresh = create_refresh_token({"sub": uid})
    return TokenResponse(access_token=access, refresh_token=refresh, user=_user_to_public(user_doc))

@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db=Depends(get_db)):
    user = await db.users.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.get("is_active"):
        raise HTTPException(status_code=403, detail="Account disabled")
    uid = str(user["_id"])
    access = create_access_token({"sub": uid})
    refresh = create_refresh_token({"sub": uid})
    return TokenResponse(access_token=access, refresh_token=refresh, user=_user_to_public(user))

@router.get("/me", response_model=UserPublic)
async def me(user=Depends(get_current_user)):
    return _user_to_public(user)

@router.post("/refresh")
async def refresh_token(creds: HTTPAuthorizationCredentials = Depends(bearer), db=Depends(get_db)):
    payload = decode_token(creds.credentials)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    access = create_access_token({"sub": payload["sub"]})
    return {"access_token": access, "token_type": "bearer"}
