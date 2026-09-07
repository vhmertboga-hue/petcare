from pydantic import BaseModel, EmailStr
from typing import Optional


class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str]
    phone_number: Optional[str]


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str]
