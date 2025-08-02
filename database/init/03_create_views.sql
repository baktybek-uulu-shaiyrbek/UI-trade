-- Audit trail for compliance
CREATE TABLE trade_audit_log (
    audit_id BIGSERIAL PRIMARY KEY,
    transaction_id BIGINT REFERENCES trading_transactions(transaction_id),
    action VARCHAR(50) NOT NULL,
    old_values JSONB,
    new_values JSONB,
    changed_by VARCHAR(100),
    changed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Aggregated statistics for performance
CREATE MATERIALIZED VIEW trading_statistics AS
SELECT 
    user_id,
    symbol_id,
    DATE_TRUNC('day', CreateDate) as trading_day,
    COUNT(*) as total_trades,
    SUM(CASE WHEN Side = 'BUY' THEN Sum ELSE 0 END) as total_bought,
    SUM(CASE WHEN Side = 'SELL' THEN Sum ELSE 0 END) as total_sold,
    AVG(Sum) as avg_trade_size
FROM trading_transactions
WHERE State = 'CLOSED'
GROUP BY user_id, symbol_id, trading_day;

-- Create indexes for the view
CREATE INDEX idx_trading_stats_user_day ON trading_statistics(user_id, trading_day);