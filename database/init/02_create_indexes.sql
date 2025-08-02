-- Optimized indexes for trading queries
CREATE INDEX idx_trading_user_date ON trading_transactions (user_id, CreateDate DESC);
CREATE INDEX idx_active_orders ON trading_transactions (OrderId, State) 
    WHERE State IN ('OPEN', 'PENDING');
CREATE INDEX idx_trading_date_brin ON trading_transactions USING BRIN (CreateDate);