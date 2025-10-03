from pydantic import BaseModel, EmailStr
from .common import BaseSchema
from .user import UserPublic

class LoginRequest(BaseSchema):
    email: EmailStr
    password: str

class SignupRequest(BaseSchema):
    email: EmailStr
    password: str
    full_name: str | None = None

class RefreshRequest(BaseSchema):
    refresh_token: str

class AuthTokens(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str | None = None

class LoginResponse(BaseModel):
    tokens: AuthTokens
    user: UserPublic

class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
