from typing import Optional

from pydantic import UUID4, BaseModel


class RegisterBaseSchema(BaseModel):
    name: str
    phone: str
    password: str

    class Config:
        orm_mode = True


class LoginMobileSchema(BaseModel):
    phone: str
    password: str

    class Config:
        orm_mode = True
        
class LoginWebSchema(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class ResetPasswordBaseSchema(BaseModel):
    user_id: str
    password: str
    new_password: str

    class Config:
        orm_mode = True

class SimpleResetPasswordSchema(BaseModel):
    phone: str
    new_password: str

class RegisterResponse(BaseModel):
    user_id: UUID4
    name: str
    phone: str

    class Config:
        orm_mode = True


class LoginResponse(BaseModel):
    user_id: UUID4
    name: str
    phone: str
    role: str
    car_seat: int
    bio: str = None
    class Config:
        orm_mode = True
