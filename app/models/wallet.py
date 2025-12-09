import uuid
import secrets
from decimal import Decimal
from sqlalchemy import String, Column, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import BaseModel


def generate_wallet_number() -> str:
    """Generate a unique 13-digit wallet number."""
    # Generate a random 13-digit number
    return ''.join([str(secrets.randbelow(10)) for _ in range(13)])


class Wallet(BaseModel):
    """Wallet model for managing user balances."""
    
    __tablename__ = "wallets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    wallet_number = Column(String(13), unique=True, nullable=False, index=True)
    balance = Column(Numeric(precision=10, scale=2), default=Decimal("0.00"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="wallet")
    transactions = relationship("Transaction", back_populates="wallet", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Wallet {self.wallet_number} Balance: {self.balance}>"
