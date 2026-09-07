from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.db.session import get_db
from backend.app.schemas.user import UserCreate, Token, UserRead
from backend.app.services.auth_service import (
    register_user,
    authenticate_user,
    create_session,
    create_session as create_session_fn,
    revoke_all_sessions_for_user,
)
from backend.app.core.security import create_access_token, create_refresh_token
from backend.app.models.user import User

router = APIRouter()


@router.post("/register", response_model=UserRead)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await register_user(db, email=data.email, phone=data.phone, password=data.password)
    return user


@router.post("/login", response_model=Token)
async def login(request: Request, data: UserCreate, db: AsyncSession = Depends(get_db)):
    identifier = data.email or data.phone
    if not identifier or not data.password:
        raise HTTPException(status_code=400, detail="Missing credentials")
    user = await authenticate_user(db, identifier, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access = create_access_token(subject=user.id)
    refresh = create_refresh_token(subject=user.id)
    await create_session(db, user, refresh, user_agent=request.headers.get("user-agent"), ip=request.client.host)

    return {"access_token": access, "refresh_token": refresh}


@router.post("/logout")
async def logout():
    # Client should delete tokens; server-side revocation via session revoke endpoint
    return {"msg": "ok"}


@router.post("/logout_all")
async def logout_all(db: AsyncSession = Depends(get_db), current_user: User = None):
    # placeholder dependency for current_user
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    await revoke_all_sessions_for_user(db, current_user)
    return {"msg": "all sessions revoked"}


@router.get("/me", response_model=UserRead)
async def me(current_user: User = None):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return current_user
