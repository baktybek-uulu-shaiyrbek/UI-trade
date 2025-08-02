from typing import List, Dict
import uuid

class DatabaseQueries:
    @staticmethod
    async def store_transaction(database, order_data: dict, user: dict):
        query = """
            INSERT INTO trading_transactions (
                CreateDate, ActiveDate, Side, Sum, Entry, State, 
                Res, PREVBAL, NEWBAL, OrderId, user_id
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            RETURNING transaction_id
        """
        
        # Get current balance
        balance = await database.fetchrow(
            "SELECT balance FROM users WHERE user_id = $1",
            user['user_id']
        )
        
        prev_balance = balance['balance']
        new_balance = prev_balance - order_data['executedQty'] * order_data['price']
        
        return await database.fetchrow(
            query,
            order_data['transactTime'],
            order_data['transactTime'],
            order_data['side'],
            order_data['executedQty'],
            order_data['price'],
            'OPEN',
            None,
            prev_balance,
            new_balance,
            order_data['orderId'],
            user['user_id']
        )
        
    @staticmethod
    async def get_trade_history(database, user_id: str) -> List[Dict]:
        query = """
            SELECT 
                transaction_id, CreateDate, ActiveDate, CloseDate,
                Side, Sum, Entry, EXIT, State, Res, PREVBAL, NEWBAL, OrderId
            FROM trading_transactions
            WHERE user_id = $1
            ORDER BY CreateDate DESC
            LIMIT 100
        """
        
        rows = await database.fetch(query, user_id)
        return [dict(row) for row in rows]
        