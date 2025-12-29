import pytest
from datetime import datetime
from uuid import uuid4
from unittest.mock import AsyncMock
from unittest.mock import AsyncMock, patch

from src.cruds import WalletCRUD
from src.models import Wallet
from src.models.enums import OperationTypeEnum
from src.schemas import WalletBase, WalletUpdateBalance, WalletForUpdateBalanceNotFound, InsufficientFundsError


@pytest.mark.asyncio
async def test_get_wallet_by_uuid_success(client):
    wallet_uuid = str(uuid4())
    mock_data = {
        "uuid": wallet_uuid,
        "balance": 100,
        "updated_at": datetime.now(),
    }

    WalletCRUD.get_by_wallet_uuid = AsyncMock(
        return_value=mock_data
    )

    response = await client.get(f"/wallets/{wallet_uuid}")
    data = response.json()

    assert response.status_code == 200
    assert data['balance'] == mock_data['balance']
    assert data['uuid'] == wallet_uuid


@pytest.mark.asyncio
async def test_get_wallet_by_uuid_not_found(client):
    wallet_uuid = str(uuid4())
    mock_data = None

    WalletCRUD.get_by_wallet_uuid = AsyncMock(
        return_value=mock_data
    )

    response = await client.get(f"/wallets/{wallet_uuid}")
    data = response.json()

    assert response.status_code == 404
    assert data['detail'] == "Wallet with this uuid not found"

@pytest.mark.asyncio
async def test_update_wallet_balance_success(client):
    wallet_uuid = str(uuid4())
    payload = WalletUpdateBalance(
        amount=100,
        operation_type=OperationTypeEnum.DEPOSIT
    )
    mock_wallet = Wallet(
        uuid=str(wallet_uuid),
        balance=200,
        updated_at=datetime.now()
    )

    WalletCRUD.update_balance = AsyncMock(return_value=mock_wallet)

    response = await client.put(f"/wallets/{wallet_uuid}/operation", json=payload.model_dump())
    data = response.json()

    assert response.status_code == 200
    assert data == {"status": "ok", "balance": 200}

@pytest.mark.asyncio
async def test_update_wallet_balance_wallet_not_found(client):
    wallet_uuid = uuid4()
    payload = WalletUpdateBalance(
        amount=100,
        operation_type=OperationTypeEnum.DEPOSIT
    )

    WalletCRUD.update_balance = AsyncMock(
        side_effect=WalletForUpdateBalanceNotFound()
    )

    response = await client.put(f"/wallets/{wallet_uuid}/operation", json=payload.model_dump())
    data = response.json()

    assert response.status_code == 400
    assert data["detail"] == "Wallet not found"

@pytest.mark.asyncio
async def test_update_wallet_balance_wallet_insufficient_funds_error(client):
    wallet_uuid = uuid4()
    payload = WalletUpdateBalance(
        amount=100,
        operation_type=OperationTypeEnum.WITHDRAW
    )

    WalletCRUD.update_balance = AsyncMock(
        side_effect=InsufficientFundsError()
    )

    response = await client.put(f"/wallets/{wallet_uuid}/operation", json=payload.model_dump())
    data = response.json()

    assert response.status_code == 400
    assert data["detail"] == "Insufficient funds"
