import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from app.config import settings


def hash_key(key: str) -> str:
    """Hash an API key or password using bcrypt."""
    return bcrypt.hashpw(key.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_key(plain_key: str, hashed_key: str) -> bool:
    """Verify a plain key against its hash."""
    return bcrypt.checkpw(
        plain_key.encode("utf-8"),
        hashed_key.encode("utf-8"),
    )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Data to encode in the token
        expires_delta: Token expiration time
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT access token.
    
    Args:
        token: JWT token to decode
        
    Returns:
        Decoded token data or None if invalid
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def parse_expiry(expiry: str) -> datetime:
    """
    Parse expiry string (1H, 1D, 1M, 1Y) to datetime.
    
    Args:
        expiry: Expiry string in format: 1H, 1D, 1M, 1Y
        
    Returns:
        Expiration datetime
    """
    value = int(expiry[:-1])
    unit = expiry[-1].upper()
    
    now = datetime.utcnow()
    
    if unit == "H":
        return now + timedelta(hours=value)
    elif unit == "D":
        return now + timedelta(days=value)
    elif unit == "M":
        return now + timedelta(days=value * 30)  # Approximate month
    elif unit == "Y":
        return now + timedelta(days=value * 365)  # Approximate year
    else:
        raise ValueError(f"Invalid expiry format: {expiry}")
