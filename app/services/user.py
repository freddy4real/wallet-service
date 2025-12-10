from typing import Optional, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.models.wallet import Wallet, generate_wallet_number
from app.utils.logger import logger


async def get_or_create_user_from_google(
    db: AsyncSession,
    email: str,
    google_id: str,
    name: str
) -> User:
    """
    Get existing user by Google ID or create new user with wallet.
    
    Args:
        db: Database session
        email: User email from Google
        google_id: Google user ID
        name: User's full name
        
    Returns:
        User model (existing or newly created)
    """
    # Check if user exists
    result = await db.execute(
        select(User).where(User.google_id == google_id)
    )
    user = result.scalar_one_or_none()
    
    if user:
        logger.info(f"Existing user logged in: {email}")
        return user
    
    logger.info(f"Creating new user: {email}")
    
    # Create new user
    user = User(
        email=email,
        google_id=google_id,
        name=name
    )
    db.add(user)
    await db.flush()  # Get user ID before creating wallet
    
    # Create wallet for new user
    wallet_number = generate_wallet_number()
    wallet = Wallet(
        user_id=user.id,
        wallet_number=wallet_number
    )
    db.add(wallet)
    
    # Commit transaction
    await db.commit()
    await db.refresh(user)
    
    logger.info(
        f"New user created successfully: {email}",
        extra={
            "user_id": str(user.id),
            "wallet_number": wallet_number,
            "google_id": google_id
        }
    )
    
    return user


async def get_user_by_id(
    db: AsyncSession,
    user_id: str
) -> Optional[User]:
    """
    Get user by ID.
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        User model or None
    """
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


async def get_user_by_email(
    db: AsyncSession,
    email: str
) -> Optional[User]:
    """
    Get user by email.
    
    Args:
        db: Database session
        email: User email
        
    Returns:
        User model or None
    """
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


async def get_user_by_google_id(
    db: AsyncSession,
    google_id: str
) -> Optional[User]:
    """
    Get user by Google ID.
    
    Args:
        db: Database session
        google_id: Google user ID
        
    Returns:
        User model or None
    """
    result = await db.execute(
        select(User).where(User.google_id == google_id)
    )
    return result.scalar_one_or_none()
