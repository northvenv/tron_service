from datetime import UTC, datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import DECIMAL, TIMESTAMP, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class WalletRequests(Base):
    __tablename__ = "wallet_requests"
    
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), 
        primary_key=True, 
        default=uuid4
    )
    wallet_address: Mapped[str] = mapped_column(String, index=True)
    bandwidth: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    energy: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    balance: Mapped[Optional[float]] = mapped_column(DECIMAL, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), 
        default=datetime.now(tz=UTC), 
        server_default=func.now()
    ) 