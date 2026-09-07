from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: Optional[EmailStr]
    phone: Optional[str]
    password: Optional[str]


class UserRead(BaseModel):
    id: int
    email: Optional[EmailStr]
    phone: Optional[str]
    is_active: bool
    role: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
