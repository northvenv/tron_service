import pytest
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy import AsyncTron

from main import create_app
from app.services.tron import TronServiceImpl
from app.services.wallet import WalletServiceImpl
from app.core.database import get_async_session
from app.api.dependencies import get_wallet_service, get_tron_service
from app.core.tron import get_tron_client
from httpx import AsyncClient, ASGITransport
from app.repositories.wallet import WalletRepository
from app.schemas.wallet import WalletInfoResponse


@pytest.fixture
def sample_wallet_data():
    return WalletInfoResponse(
        wallet_address = "TNPeeaaFB7K9cmo4uQpcU32zGK8G1NYqeL",
        bandwidth = 0,
        energy = 0,
        balance = 0.0,
    )

@pytest.fixture
def mock_account():
    return {
        'net_window_size': 500,
        'account_resource': {
            'acquired_delegated_frozenV2_balance_for_energy': 200_000_000
        }
    }

@pytest.fixture
def mock_wallet_repository():
    return AsyncMock(spec=WalletRepository)

@pytest.fixture
def mock_tron_client():
    return AsyncMock(spec=AsyncTron)

@pytest.fixture
def mock_db_session():
    session = AsyncMock(spec=AsyncSession)
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    return session

@pytest.fixture
def mock_tron_service(mock_tron_client):
    return AsyncMock(spec=TronServiceImpl)

@pytest.fixture
def mock_wallet_service(mock_db_session):
    return AsyncMock(spec=WalletServiceImpl)

@pytest.fixture
async def client(mock_tron_client, mock_db_session, mock_tron_service, mock_wallet_service):
    app = create_app()
    app.dependency_overrides.update({
        get_tron_client: lambda: mock_tron_client,
        get_async_session: lambda: mock_db_session,
        get_tron_service: lambda _: mock_tron_service,
        get_wallet_service: lambda _: mock_wallet_service
    })
    
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:
        yield ac
    
    app.dependency_overrides.clear()
