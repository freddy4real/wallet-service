from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from uuid import UUID


class WalletResponse(BaseModel):
    """Schema for wallet response."""
    id: UUID
    wallet_number: str
    balance: Decimal
    created_at: datetime
    
    class Config:
        from_attributes = True


class BalanceResponse(BaseModel):
    """Schema for balance response."""
    balance: Decimal


class DepositRequest(BaseModel):
    """Schema for deposit request."""
    amount: Decimal = Field(..., gt=0, description="Amount to deposit (must be positive)")


class DepositResponse(BaseModel):
    """Schema for deposit response."""
    reference: str
    authorization_url: str


class TransferRequest(BaseModel):
    """Schema for wallet transfer request."""
    wallet_number: str = Field(..., min_length=13, max_length=13)
    amount: Decimal = Field(..., gt=0, description="Amount to transfer (must be positive)")


class TransferResponse(BaseModel):
    """Schema for transfer response."""
    status: str
    message: str
