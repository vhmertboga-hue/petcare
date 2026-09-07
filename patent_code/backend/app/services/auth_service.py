from datetime import timedelta
from typing import Optional
import hashlib

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from backend.app.models.user import User
from backend.app.models.session import Session


REFRESH_EXPIRES_DAYS = 30


async def register_user(db: AsyncSession, email: Optional[str], phone: Optional[str], password: Optional[str]):
    user = User(email=email, phone=phone)
    if password:
        user.hashed_password = get_password_hash(password)
    db.add(user)
    await db.flush()
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, email_or_phone: str, password: str) -> Optional[User]:
    q = None
    if "@" in email_or_phone:
        q = select(User).where(User.email == email_or_phone)
    else:
        q = select(User).where(User.phone == email_or_phone)

    r = await db.execute(q)
    user = r.scalars().first()
    if not user or not user.hashed_password:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


async def create_session(db: AsyncSession, user: User, refresh_token: str, user_agent: Optional[str] = None, ip: Optional[str] = None):
    h = _hash_token(refresh_token)
    s = Session(user_id=user.id, refresh_token_hash=h, user_agent=user_agent, ip_address=ip)
    db.add(s)
    await db.flush()
    await db.commit()
    await db.refresh(s)
    return s


async def revoke_session(db: AsyncSession, session_id: int):
    q = select(Session).where(Session.id == session_id)
    r = await db.execute(q)
    s = r.scalars().first()
    if s:
        s.revoked = True
        db.add(s)
        await db.commit()
    return s


async def revoke_all_sessions_for_user(db: AsyncSession, user: User):
    await db.execute("UPDATE sessions SET revoked = true WHERE user_id = :uid", {"uid": user.id})
    await db.commit()
from datetime import timedelta, datetime
from backend.app.models.user import User, RoleEnum
from backend.app.models.refresh_token import RefreshToken
from backend.app.models.otp import OTP
from backend.app.models.audit import AuditLog
from backend.app.core.security import hash_password, verify_password, create_jwt_token, decode_jwt_token
from backend.app.db.session import SessionLocal
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import secrets


def create_user(db: Session, email: str, password: str, full_name: str = None, phone: str = None):
    user = User(email=email.lower(), hashed_password=hash_password(password), full_name=full_name, phone_number=phone)
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        return None


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email.lower()).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_tokens_for_user(db: Session, user: User, device_info: dict = None):
    access_token, at_jti = create_jwt_token(subject=str(user.id), expires_delta=timedelta(minutes=15))
    refresh_token, rt_jti = create_jwt_token(subject=str(user.id), expires_delta=timedelta(days=30))
    rt = RefreshToken(jti=rt_jti, user_id=user.id, user_agent=device_info.get("user_agent") if device_info else None, ip_address=device_info.get("ip") if device_info else None, expires_at=datetime.utcnow() + timedelta(days=30))
    db.add(rt)
    db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token}


def revoke_refresh_token(db: Session, jti: str):
    rt = db.query(RefreshToken).filter(RefreshToken.jti == jti).first()
    if rt:
        db.delete(rt)
        db.commit()


def revoke_all_refresh_tokens(db: Session, user_id: int):
    db.query(RefreshToken).filter(RefreshToken.user_id == user_id).delete()
    db.commit()


def create_otp(db: Session, phone: str = None, user_id: int = None, purpose: str = "phone_verify"):
    code = str(secrets.randbelow(10**6)).zfill(6)
    expires = datetime.utcnow() + timedelta(minutes=5)
    otp = OTP(user_id=user_id, phone=phone, code=code, purpose=purpose, expires_at=expires)
    db.add(otp)
    db.commit()
    db.refresh(otp)
    return otp


def verify_otp(db: Session, phone: str = None, code: str = None, purpose: str = "phone_verify"):
    now = datetime.utcnow()
    q = db.query(OTP).filter(OTP.code == code, OTP.purpose == purpose, OTP.expires_at > now)
    if phone:
        q = q.filter(OTP.phone == phone)
    otp = q.first()
    if otp:
        db.delete(otp)
        db.commit()
        return True
    return False


def write_audit(db: Session, user_id: int = None, action: str = None, details: str = None, ip: str = None, ua: str = None):
    a = AuditLog(user_id=user_id, action=action, details=details, ip_address=ip, user_agent=ua)
    db.add(a)
    db.commit()
