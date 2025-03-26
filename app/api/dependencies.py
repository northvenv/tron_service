from sqlalchemy.ext.asyncio import AsyncSession
from tronpy import AsyncTron

from app.repositories.wallet import WalletRepository
from app.services.tron import TronService, TronServiceImpl
from app.services.wallet import WalletService, WalletServiceImpl


def get_wallet_service(
    session: AsyncSession
) -> WalletService:
    return WalletServiceImpl(
        repository=WalletRepository(
            session=session
        )
    )

def get_tron_service(
    tron_client: AsyncTron
) -> TronService:
    return TronServiceImpl(client=tron_client)