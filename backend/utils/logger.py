class TradingError(Exception):
    """Base exception for trading operations"""
    pass

class AuthenticationError(TradingError):
    """Raised when authentication fails"""
    pass

class OrderError(TradingError):
    """Raised when order placement fails"""
    pass

class InsufficientBalanceError(TradingError):
    """Raised when user has insufficient balance"""
    pass