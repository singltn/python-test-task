class InsufficientFundsError(Exception):
    def __init__(self):
        super().__init__("Insufficient funds")

class InvalidOperationError(Exception):
    def __init__(self):
        super().__init__("Invalid operation")

class WalletForUpdateBalanceNotFound(Exception):
    def __init__(self):
        super().__init__("Wallet not found")