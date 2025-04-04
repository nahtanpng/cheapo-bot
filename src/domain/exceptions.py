class GamblingException(Exception):
    """Base exception for gambling-related errors"""
    pass

class InsufficientBalanceException(GamblingException):
    def __init__(self, current_balance: int):
        self.current_balance = current_balance
        super().__init__(f"You only have {current_balance} coins!")

class InvalidAmountException(GamblingException):
    pass

class SelfPaymentException(GamblingException):
    pass