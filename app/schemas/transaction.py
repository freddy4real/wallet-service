from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from uuid import UUID
from app.models.transaction import TransactionType, TransactionStatus


class TransactionResponse(BaseModel):
    """Schema for transaction response."""
    id: UUID
    type: TransactionType
    amount: Decimal
    reference: str
    status: TransactionStatus
    created_at: datetime
    
    class Config:
        from_attributes = True


class DepositStatusResponse(BaseModel):
    """Schema for deposit status check."""
    reference: str
    status: TransactionStatus
    amount: Decimal
