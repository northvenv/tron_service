from abc import abstractmethod
from typing import Protocol, Sequence

from app.models.wallet import WalletRequests
from app.repositories.wallet import WalletRepository
from app.schemas.wallet import WalletInfoResponse, WalletRequestRecord


class WalletService(Protocol):
    @abstractmethod
    async def save(self, data: WalletInfoResponse) -> None:
        pass

    @abstractmethod
    async def get(
        self, 
        skip: int = 0, 
        limit: int = 15
    ) -> Sequence[WalletRequests]:
        pass


class WalletServiceImpl:
    def __init__(self, repository: WalletRepository):
        self.repository: WalletRepository = repository

    async def save(self, data: WalletInfoResponse) -> None:
        await self.repository.save(data)

    async def get(
        self, 
        skip: int = 0, 
        limit: int = 15
    ) -> list[WalletRequestRecord]:
        requests = await self.repository.get(skip, limit)
        return [WalletRequestRecord.model_validate(item) for item in requests]

    