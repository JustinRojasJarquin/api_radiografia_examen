from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class GoogleLoginRequest(BaseModel):
    token: str = Field(..., min_length=10)


class AuthUserResponse(BaseModel):
    id: int
    email: str
    name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class GoogleLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: AuthUserResponse
