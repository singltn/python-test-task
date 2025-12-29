from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from src.models.enums import OperationTypeEnum


class WalletBase(BaseModel):
    uuid: str
    balance: float
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class WalletUpdateBalance(BaseModel):
    operation_type: OperationTypeEnum
    amount: int = Field(gt=0)