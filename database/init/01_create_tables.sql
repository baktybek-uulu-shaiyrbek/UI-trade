CREATE TABLE trading_transactions (
    transaction_id BIGSERIAL PRIMARY KEY,
    CreateDate TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ActiveDate TIMESTAMPTZ,
    CloseDate TIMESTAMPTZ,
    Side VARCHAR(4) NOT NULL CHECK (Side IN ('BUY', 'SELL')),
    Sum NUMERIC(20,8) NOT NULL,
    Entry NUMERIC(20,8) NOT NULL,
    EXIT NUMERIC(20,8),
    State VARCHAR(20) NOT NULL CHECK (State IN ('PENDING', 'OPEN', 'CLOSED', 'CANCELLED')),
    Res VARCHAR(100),
    PREVBAL NUMERIC(20,8) NOT NULL,
    NEWBAL NUMERIC(20,8) NOT NULL,
    OrderId UUID NOT NULL UNIQUE,
    symbol_id INTEGER,
    user_id INTEGER,
    CONSTRAINT valid_dates CHECK (CloseDate IS NULL OR CloseDate >= ActiveDate),
    CONSTRAINT balance_consistency CHECK (
        NEWBAL = PREVBAL + CASE WHEN Side = 'BUY' THEN -Sum ELSE Sum END
    )
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    balance NUMERIC(20,8) DEFAULT 15000,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE symbols (
    symbol_id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) UNIQUE NOT NULL,
    base_asset VARCHAR(10) NOT NULL,
    quote_asset VARCHAR(10) NOT NULL
);