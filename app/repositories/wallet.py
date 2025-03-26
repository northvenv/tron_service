from typing import Sequence, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wallet import WalletRequests
from app.schemas.wallet import WalletInfoResponse


class WalletRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model: Type[WalletRequests] = WalletRequests

    async def save(self, data: WalletInfoResponse) -> None:
        instance = self.model(**data.model_dump())
        self.session.add(instance)
        await self.session.commit()

    async def get(
        self, 
        skip: int = 0, 
        limit: int = 15
    ) -> Sequence[WalletRequests]:
        requests_query = select(
            self.model
        ).order_by(
            self.model.created_at.desc()
        ).offset(skip).limit(limit)
        requests_result = await self.session.execute(requests_query)
        return requests_result.scalars().all()
    

