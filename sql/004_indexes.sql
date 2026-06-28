-- ==========================
-- FACT TRANSACTIONS
-- ==========================

CREATE INDEX IF NOT EXISTS idx_fact_user
ON gold.fact_transactions(user_key);

CREATE INDEX IF NOT EXISTS idx_fact_card
ON gold.fact_transactions(card_key);

CREATE INDEX IF NOT EXISTS idx_fact_merchant
ON gold.fact_transactions(merchant_key);

CREATE INDEX IF NOT EXISTS idx_fact_date
ON gold.fact_transactions(date_key);

CREATE INDEX IF NOT EXISTS idx_fact_time
ON gold.fact_transactions(time_key);

CREATE INDEX IF NOT EXISTS idx_fact_is_fraud
ON gold.fact_transactions(is_fraud);

CREATE INDEX IF NOT EXISTS idx_fact_date_fraud
ON gold.fact_transactions(date_key, is_fraud);

-- ==========================
-- DIMENSIONS (WHERE, JOIN, Composite Indexes)
-- ==========================

CREATE INDEX IF NOT EXISTS idx_dim_users_user
ON gold.dim_users(user_id);

CREATE INDEX IF NOT EXISTS idx_dim_cards_user_card
ON gold.dim_cards(user_id, card_index);

CREATE UNIQUE INDEX uq_dim_merchants
ON gold.dim_merchants (
    merchant_name,
    merchant_city,
    merchant_state,
    zipcode,
    mcc
)
NULLS NOT DISTINCT;