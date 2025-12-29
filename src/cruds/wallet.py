from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from pydantic import UUID4

from src.models import Wallet
from src.models.enums import OperationTypeEnum
from src.schemas import InsufficientFundsError, InvalidOperationError, WalletForUpdateBalanceNotFound


class WalletCRUD:
    model = Wallet

    @classmethod
    async def get_by_wallet_uuid(
            cls,
            session: AsyncSession,
            uuid: UUID4
    ) -> Optional[Wallet]:
        query = select(cls.model).where(cls.model.uuid == str(uuid))
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def update_balance(
            cls,
            session: AsyncSession,
            uuid: UUID4,
            amount: int,
            operation_type: OperationTypeEnum,
    ) -> Wallet:
        result = await session.execute(
            select(Wallet).where(Wallet.uuid == str(uuid)).with_for_update()
        )
        wallet = result.scalar_one_or_none()
        if not wallet:
            raise WalletForUpdateBalanceNotFound()

        if operation_type == OperationTypeEnum.DEPOSIT:
            new_balance = wallet.balance + amount
        elif operation_type == OperationTypeEnum.WITHDRAW:
            if wallet.balance < amount:
                raise InsufficientFundsError
            new_balance = wallet.balance - amount
        else:
            raise InvalidOperationError

        wallet.balance = new_balance
        await session.commit()
        await session.refresh(wallet)
        return wallet
