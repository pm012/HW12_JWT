
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field



class ContactBase(BaseModel):
    name: str = Field(max_length=30)
    surname: str = Field(max_length=30)
    email: EmailStr
    phone: str = Field(max_length=20)
    birth_date: datetime    
    additional_data: Optional[str] = Field(max_length=150, default=None)


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    name: Optional[str] = Field(max_length=30, default=None)
    surname: Optional[str] = Field(max_length=30, default=None)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(max_length=20, default=None)
    birth_date: Optional[datetime] = None
    additional_data: Optional[str] = Field(max_length=150, default=None)


class ContactResponse(ContactBase):
    id: int

    class Config:
        #orm_mode = True
        from_attributes = True


class UserModel(BaseModel):
    username: str = Field(min_length=4, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        #orm_mode = True
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RequestEmail(BaseModel):
    email: EmailStr

