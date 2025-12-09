from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import List, Literal


class APIKeyCreate(BaseModel):
    """Schema for creating an API key."""
    name: str = Field(..., min_length=1, max_length=100)
    permissions: List[Literal["deposit", "transfer", "read"]] = Field(..., min_items=1)
    expiry: Literal["1H", "1D", "1M", "1Y"]


class APIKeyResponse(BaseModel):
    """Schema for API key response (only shown once)."""
    api_key: str
    expires_at: datetime


class APIKeyInfo(BaseModel):
    """Schema for listing API key information (without the actual key)."""
    id: UUID
    name: str
    permissions: List[str]
    expires_at: datetime
    revoked: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class APIKeyRollover(BaseModel):
    """Schema for rolling over an expired API key."""
    expired_key_id: UUID
    expiry: Literal["1H", "1D", "1M", "1Y"]
