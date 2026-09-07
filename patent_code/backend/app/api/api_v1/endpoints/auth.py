from fastapi import APIRouter, Depends, HTTPException, status, Request, Body
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
from backend.app.models.session import Session as SessionModel
from backend.app.models.otp import OTP as OTPModel
from datetime import datetime, timedelta
import secrets
from backend.app.services.auth_service import _hash_token
from backend.app.core.security import decode_token, get_password_hash

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


@router.post("/refresh", response_model=Token)
async def refresh(payload: dict = Body(...), db: AsyncSession = Depends(get_db), request: Request = None):
    """Rotate refresh token and issue a new access token."""
    refresh_token = payload.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Missing refresh_token")
    # decode token to get subject
    try:
        data = decode_token(refresh_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    sub = data.get("sub")
    if not sub:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # find session by hashed token
    h = _hash_token(refresh_token)
    q = select(SessionModel).where(SessionModel.refresh_token_hash == h, SessionModel.revoked == False)
    r = await db.execute(q)
    s = r.scalars().first()
    if not s:
        raise HTTPException(status_code=401, detail="Session not found or revoked")

    # issue new tokens and rotate session
    access = create_access_token(subject=sub)
    new_refresh = create_refresh_token(subject=sub)
    # revoke old session and create new session record
    await revoke_all_sessions_for_user(db, s.user)
    await create_session(db, s.user, new_refresh, user_agent=request.headers.get("user-agent") if request else None, ip=request.client.host if request else None)

    return {"access_token": access, "refresh_token": new_refresh}


@router.post("/otp/request")
async def otp_request(data: dict = Body(...), db: AsyncSession = Depends(get_db)):
    """Create and return an OTP for phone verification or password reset (scaffold).
    This returns the code directly for dev/testing; integrate SMS/email in production."""
    phone = data.get("phone")
    user_id = data.get("user_id")
    purpose = data.get("purpose", "phone_verify")
    if not phone and not user_id:
        raise HTTPException(status_code=400, detail="phone or user_id required")
    # generate 6-digit code
    code = str(secrets.randbelow(10**6)).zfill(6)
    expires = datetime.utcnow() + timedelta(minutes=5)
    otp = OTPModel(user_id=user_id, phone=phone, code=code, purpose=purpose, expires_at=expires)
    db.add(otp)
    await db.flush()
    await db.commit()
    return {"code": code, "expires_at": expires.isoformat()}


@router.post("/otp/verify")
async def otp_verify(data: dict = Body(...), db: AsyncSession = Depends(get_db)):
    phone = data.get("phone")
    code = data.get("code")
    purpose = data.get("purpose", "phone_verify")
    if not code:
        raise HTTPException(status_code=400, detail="code required")
    q = select(OTPModel).where(OTPModel.code == code, OTPModel.purpose == purpose, OTPModel.expires_at > datetime.utcnow())
    if phone:
        q = q.where(OTPModel.phone == phone)
    r = await db.execute(q)
    otp = r.scalars().first()
    if not otp:
        raise HTTPException(status_code=400, detail="Invalid or expired code")
    # consume otp
    await db.delete(otp)
    await db.commit()
    return {"ok": True}


@router.post("/password-reset/request")
async def password_reset_request(data: dict = Body(...), db: AsyncSession = Depends(get_db)):
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="email required")
    q = select(User).where(User.email == email)
    r = await db.execute(q)
    user = r.scalars().first()
    if not user:
        # do not reveal user existence
        return {"ok": True}
    # create OTP for password reset
    code = str(secrets.randbelow(10**6)).zfill(6)
    expires = datetime.utcnow() + timedelta(minutes=15)
    otp = OTPModel(user_id=user.id, phone=None, code=code, purpose="password_reset", expires_at=expires)
    db.add(otp)
    await db.flush()
    await db.commit()
    # In production, send code via email. For now return code.
    return {"code": code}


@router.post("/password-reset/confirm")
async def password_reset_confirm(data: dict = Body(...), db: AsyncSession = Depends(get_db)):
    email = data.get("email")
    code = data.get("code")
    new_password = data.get("new_password")
    if not (email and code and new_password):
        raise HTTPException(status_code=400, detail="email, code and new_password required")
    q = select(OTPModel).where(OTPModel.code == code, OTPModel.purpose == "password_reset", OTPModel.expires_at > datetime.utcnow())
    r = await db.execute(q)
    otp = r.scalars().first()
    if not otp:
        raise HTTPException(status_code=400, detail="Invalid or expired code")
    # find user
    q2 = select(User).where(User.id == otp.user_id, User.email == email)
    r2 = await db.execute(q2)
    user = r2.scalars().first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user")
    user.hashed_password = get_password_hash(new_password)
    db.add(user)
    await db.delete(otp)
    await db.commit()
    return {"ok": True}


@router.post("/social/{provider}")
async def social_login(provider: str, data: dict = Body(...), db: AsyncSession = Depends(get_db)):
    """Scaffold for social login (Google/Apple). Implement provider token verification and user creation here."""
    # data may contain provider_token, etc.
    return {"detail": "social login not implemented yet", "provider": provider}
