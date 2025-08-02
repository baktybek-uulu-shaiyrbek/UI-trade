from datetime import datetime
from decimal import Decimal
import uuid

class TradingTransaction:
    def __init__(self):
        self.transaction_id = None
        self.create_date = datetime.utcnow()
        self.active_date = None
        self.close_date = None
        self.side = None  # BUY or SELL
        self.sum = Decimal('0')
        self.entry = Decimal('0')
        self.exit = None
        self.state = 'PENDING'  # PENDING, OPEN, CLOSED, CANCELLED
        self.res = None
        self.prevbal = Decimal('0')
        self.newbal = Decimal('0')
        self.order_id = str(uuid.uuid4())
        self.symbol_id = None
        self.user_id = None