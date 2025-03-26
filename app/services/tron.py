from abc import abstractmethod
from typing import Protocol

from tronpy import AsyncTron

from app.schemas.wallet import WalletInfoResponse


class TronService(Protocol):
    @abstractmethod
    async def get_wallet_info(self, address: str) -> WalletInfoResponse:
        pass

class TronServiceImpl:
    def __init__(self, client: AsyncTron):
        self.client = client

    async def get_wallet_info(self, address: str) -> WalletInfoResponse:
        try:
            account = await self.client.get_account(address)
            balance = await self.client.get_account_balance(address)

            bandwidth = account.get('net_window_size', 0)
            energy = account.get(
                'account_resource', {}
            ).get(
                'acquired_delegated_frozenV2_balance_for_energy', 0
            ) // 1_000_000 

            return WalletInfoResponse(
                wallet_address=address,
                bandwidth=bandwidth,
                energy=energy,
                balance=balance
            )
        except Exception as e:
            raise ValueError(f"Error fetching wallet info: {str(e)}")