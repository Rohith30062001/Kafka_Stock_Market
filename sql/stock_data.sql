CREATE TABLE stock_data (
    id SERIAL PRIMARY KEY,        -- Auto-incrementing ID
    timestamp TIMESTAMP NOT NULL, -- Datetime of stock price
    open DECIMAL(10,2) NOT NULL,  -- Opening price
    high DECIMAL(10,2) NOT NULL,  -- Highest price
    low DECIMAL(10,2) NOT NULL,   -- Lowest price
    close DECIMAL(10,2) NOT NULL, -- Closing price
    volume BIGINT NOT NULL,       -- Trading volume
    created_at TIMESTAMP DEFAULT NOW(), -- When the record was inserted
    UNIQUE (timestamp)            -- Prevent duplicate entries
);