from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    is_admin: bool = False


class UserCreate(UserBase):
    email: EmailStr
    password: str
    tenant_id: int


class UserRead(UserBase):
    id: int
    tenant_id: int

    class Config:
        from_attributes = True
