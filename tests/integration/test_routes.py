import pytest
from fastapi import status
from httpx import AsyncClient
from unittest.mock import AsyncMock


@pytest.mark.asyncio
@pytest.mark.parametrize("wallet_address", [
    "TNPeeaaFB7K9cmo4uQpcU32zGK8G1NYqeL",
    "TWd4WrZ9wn84f5x1hZhL4DHvk738ns5jwb"
])
async def test_multiple_wallet_addresses(client: AsyncClient, mock_account, mock_tron_client, wallet_address):
    mock_tron_client.get_account = AsyncMock(return_value=mock_account)
    mock_tron_client.get_account_balance = AsyncMock(return_value=1000.0)
    
    response = await client.post(
        "/wallet/info",
        json={"wallet_address": wallet_address}
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "wallet_address": wallet_address,
        "bandwidth": 500,
        "energy": 200,
        "balance": 1000.0
    }
    
    mock_tron_client.get_account.assert_awaited_once_with(wallet_address)
    mock_tron_client.get_account_balance.assert_awaited_once_with(wallet_address)


@pytest.mark.asyncio
@pytest.mark.parametrize("wallet_address", [
    "TNPeeaaFB7K9c",   
    "TWd4WrZ9wn84f5"
])
@pytest.mark.asyncio
async def test_get_wallet_info_validation(client: AsyncClient, wallet_address):
    response = await client.post(
        "/wallet/info",
        json={"wallet_address": wallet_address}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


