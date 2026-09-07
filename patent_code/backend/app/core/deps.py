from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.app.core.security import decode_jwt_token
from backend.app.models.user import User
from importlib import import_module

security = HTTPBearer()


def get_db():
    # Obtain the sessionmaker at call time so test-time patches to the
    # session module are respected (conftest may replace SessionLocal).
    db_module = import_module("backend.app.db.session")
    SessionLocal = getattr(db_module, "SessionLocal")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db=Depends(get_db)):
    token = credentials.credentials
    payload = decode_jwt_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth token")
    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
