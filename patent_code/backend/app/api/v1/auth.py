from fastapi import APIRouter, Depends, HTTPException, status, Request
from backend.app.schemas.auth import RegisterIn, LoginIn, TokenOut
from backend.app.db.session import SessionLocal
from backend.app.services.auth_service import create_user, authenticate_user, create_tokens_for_user, write_audit, revoke_refresh_token, revoke_all_refresh_tokens, create_otp, verify_otp
from backend.app.models.user import User
from sqlalchemy.orm import Session
from typing import Dict

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=TokenOut)
def register(payload: RegisterIn, request: Request, db: Session = Depends(get_db)):
    user = create_user(db, email=payload.email, password=payload.password, full_name=payload.full_name, phone=payload.phone_number)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")
    tokens = create_tokens_for_user(db, user, device_info={"user_agent": request.headers.get("user-agent"), "ip": request.client.host})
    write_audit(db, user_id=user.id, action="register", details="user registered", ip=request.client.host, ua=request.headers.get("user-agent"))
    return {"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"]}


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, request: Request, db: Session = Depends(get_db)):
    user = authenticate_user(db, email=payload.email, password=payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    tokens = create_tokens_for_user(db, user, device_info={"user_agent": request.headers.get("user-agent"), "ip": request.client.host})
    write_audit(db, user_id=user.id, action="login", details="user logged in", ip=request.client.host, ua=request.headers.get("user-agent"))
    return {"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"]}


@router.post("/logout")
def logout(body: Dict[str, str], request: Request, db: Session = Depends(get_db)):
    token_jti = body.get("token_jti")
    if not token_jti:
        raise HTTPException(status_code=400, detail="token_jti required")
    revoke_refresh_token(db, token_jti)
    write_audit(db, action="logout", details=f"revoked {token_jti}", ip=request.client.host, ua=request.headers.get("user-agent"))
    return {"detail": "logged out"}


@router.post("/logout_all")
def logout_all(request: Request, user_id: int, db: Session = Depends(get_db)):
    revoke_all_refresh_tokens(db, user_id)
    write_audit(db, user_id=user_id, action="logout_all", details="revoked all refresh tokens", ip=request.client.host, ua=request.headers.get("user-agent"))
    return {"detail": "all sessions revoked"}


@router.post("/otp/send")
def send_otp(phone: str, db: Session = Depends(get_db)):
    otp = create_otp(db, phone=phone)
    # In production: send via SMS provider
    print(f"OTP for {phone}: {otp.code}")
    return {"detail": "otp_sent"}


@router.post("/otp/verify")
def verify_otp_endpoint(phone: str, code: str, db: Session = Depends(get_db)):
    ok = verify_otp(db, phone=phone, code=code)
    if not ok:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    return {"detail": "verified"}
