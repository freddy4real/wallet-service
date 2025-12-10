from decimal import Decimal
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Transaction, TransactionType, TransactionStatus


async def create_pending_transaction(
    db: AsyncSession,
    wallet_id: str,
    amount: Decimal,
    reference: str
) -> Transaction:
    """
    Create a pending deposit transaction.
    
    Args:
        db: Database session
        wallet_id: Wallet ID
        amount: Transaction amount
        reference: Unique transaction reference
        
    Returns:
        Created transaction
    """
    transaction = Transaction(
        wallet_id=wallet_id,
        type=TransactionType.DEPOSIT,
        amount=amount,
        reference=reference,
        status=TransactionStatus.PENDING
    )
    
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    
    return transaction


async def get_transaction_by_reference(
    db: AsyncSession,
    reference: str
) -> Optional[Transaction]:
    """
    Get a transaction by reference.
    
    Args:
        db: Database session
        reference: Transaction reference
        
    Returns:
        Transaction model or None
    """
    result = await db.execute(
        select(Transaction).where(Transaction.reference == reference)
    )
    return result.scalar_one_or_none()


async def update_transaction_status(
    db: AsyncSession,
    transaction: Transaction,
    status: TransactionStatus
) -> Transaction:
    """
    Update transaction status.
    
    Args:
        db: Database session
        transaction: Transaction to update
        status: New status
        
    Returns:
        Updated transaction
    """
    transaction.status = status
    await db.commit()
    await db.refresh(transaction)
    
    return transaction
