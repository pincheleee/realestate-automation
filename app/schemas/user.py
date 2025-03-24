from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.user import UserRole
from .base import BaseSchema

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    role: UserRole = UserRole.USER
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class UserInDB(UserBase, BaseSchema):
    pass

class User(UserInDB):
    pass

class UserWithProperties(User):
    properties_count: int = 0
    leads_count: int = 0
    appointments_count: int = 0 