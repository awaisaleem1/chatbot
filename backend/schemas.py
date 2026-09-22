from typing import Literal

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr


class LoginResponse(BaseModel):
    success: bool
    message: str


class UserCreate(BaseModel):
    name: str | None = None
    email: EmailStr
    phone: str | None = None
    city: str | None = None


class UserResponse(BaseModel):
    id: int
    name: str | None
    email: str
    phone: str | None
    city: str | None

    class Config:
        from_attributes = True


class UserCommand(BaseModel):
    action: Literal[
        "create_user",
        "update_user",
        "delete_user",
        "get_user",
        "list_users"
    ]

    # User identification
    email: str | None = None
    identifier: str | None = None

    # Create-user fields
    name: str | None = None
    phone: str | None = None
    city: str | None = None

    # Update-user fields
    field: Literal[
        "name",
        "email",
        "phone",
        "city"
    ] | None = None

    value: str | None = None