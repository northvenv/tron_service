from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator
from tronpy.keys import is_address


class WalletInfoRequest(BaseModel):
    wallet_address: str

    @field_validator('wallet_address')
    def validate_tron_address(cls, v):
        if not is_address(v):
            raise ValueError('bad base58check format')
        return v

class WalletInfoResponse(BaseModel):
    wallet_address: str
    bandwidth: Optional[int]
    energy: Optional[int]
    balance: float

    class Config:
        from_attributes = True

class WalletRequestRecord(BaseModel):
    id: UUID
    wallet_address: str
    bandwidth: Optional[int] = None
    energy: Optional[int] = None
    balance: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True

