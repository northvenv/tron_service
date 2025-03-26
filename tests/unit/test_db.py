import pytest
from app.models.wallet import WalletRequests
from app.repositories.wallet import WalletRepository


@pytest.mark.asyncio
async def test_save_wallet(mock_db_session, sample_wallet_data):
    repo = WalletRepository(mock_db_session)
    
    await repo.save(sample_wallet_data)
    
    mock_db_session.add.assert_called_once()
    
    added_instance = mock_db_session.add.call_args[0][0]
    
    assert isinstance(added_instance, WalletRequests)
    
    assert added_instance.wallet_address == sample_wallet_data.wallet_address
    assert added_instance.bandwidth == sample_wallet_data.bandwidth
    assert added_instance.energy == sample_wallet_data.energy
    assert added_instance.balance == sample_wallet_data.balance
    
    mock_db_session.commit.assert_awaited_once()