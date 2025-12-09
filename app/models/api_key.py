import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Column, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import BaseModel


class APIKey(BaseModel):
    """API Key model for service-to-service authentication."""
    
    __tablename__ = "api_keys"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    key_prefix = Column(String, index=True, nullable=False)
    key_hash = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    permissions = Column(JSON, nullable=False)  # List of permissions: ["deposit", "transfer", "read"]
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="api_keys")
    
    def __repr__(self):
        return f"<APIKey {self.name} User: {self.user_id}>"
    
    def is_valid(self) -> bool:
        """Check if API key is valid (not expired and not revoked)."""
        return not self.revoked and datetime.utcnow() < self.expires_at
