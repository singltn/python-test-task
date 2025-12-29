from enum import Enum


class OperationTypeEnum(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
