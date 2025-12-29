from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

from src.core.database import get_db
from src import schemas

from src.cruds import WalletCRUD

router = APIRouter(prefix="/wallets", tags=["wallets"])


@router.get(
    "/{uuid}",
    status_code=200,
    response_model=schemas.WalletBase,
)
async def get_wallet_by_uuid(
        uuid: UUID4 = Path(..., description="The uuid of wallet"),
        session: AsyncSession = Depends(get_db),
):
    wallet = await WalletCRUD.get_by_wallet_uuid(session, uuid)
    if not wallet:
        raise HTTPException(
            status_code=404,
            detail="Wallet with this uuid not found"
        )
    return wallet


@router.put(
    "/{uuid}/operation",
    status_code=200,
    response_model=dict,

)
async def update_wallet_balance(
        payload: schemas.WalletUpdateBalance,
        uuid: UUID4 = Path(..., description="The uuid of wallet"),
        session: AsyncSession = Depends(get_db),
):
    try:
        wallet = await WalletCRUD.update_balance(session, uuid, payload.amount, payload.operation_type)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    return {
        "status": "ok",
        "balance": wallet.balance,
    }
