from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy import AsyncTron

from app.api.dependencies import get_tron_service, get_wallet_service
from app.core.database import get_async_session
from app.core.tron import get_tron_client
from app.schemas.wallet import (
    WalletInfoRequest,
    WalletInfoResponse,
    WalletRequestRecord,
)

router = APIRouter(prefix="/wallet")


@router.post("/info", response_model=WalletInfoResponse)
async def get_wallet_info(
    data: WalletInfoRequest,
    tron_client: AsyncTron = Depends(get_tron_client),
    session: AsyncSession = Depends(get_async_session)
) -> WalletInfoResponse:
    tron_service = get_tron_service(tron_client)
    wallet_service = get_wallet_service(session)
    
    try:
        wallet_data = await tron_service.get_wallet_info(
            data.wallet_address
        )
        await wallet_service.save(
            data=wallet_data
        )
        return wallet_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/requests", response_model=list[WalletRequestRecord])
async def get_wallet_requests(
    skip: int = 0, 
    limit: int = 10, 
    session: AsyncSession = Depends(get_async_session)
):
    wallet_service = get_wallet_service(session=session)
    result = await wallet_service.get(skip=skip, limit=limit)
    return result

