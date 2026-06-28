DROP TABLE IF EXISTS gold.fact_transactions CASCADE;

-- =========================
-- FACT TRANSACTIONS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS gold.fact_transactions (
    transaction_key   BIGINT  PRIMARY KEY,
    user_key          INTEGER NOT NULL,
    card_key          INTEGER NOT NULL,
    merchant_key      INTEGER NOT NULL,
    date_key          INTEGER NOT NULL,
    time_key          INTEGER NOT NULL,

    amount            NUMERIC(12,2),
    use_chip          VARCHAR(50),
    errors            TEXT,
    is_fraud          BOOLEAN,

    CONSTRAINT fk_fact_user
        FOREIGN KEY (user_key)
        REFERENCES gold.dim_users(user_key),

    CONSTRAINT fk_fact_card
        FOREIGN KEY (card_key)
        REFERENCES gold.dim_cards(card_key),

    CONSTRAINT fk_fact_merchant
        FOREIGN KEY (merchant_key)
        REFERENCES gold.dim_merchants(merchant_key),

    CONSTRAINT fk_fact_date
        FOREIGN KEY (date_key)
        REFERENCES gold.dim_date(date_key),

    CONSTRAINT fk_fact_time
        FOREIGN KEY (time_key)
        REFERENCES gold.dim_time(time_key)
);

-- =========================
-- INSERT FACT DATA
-- =========================
INSERT INTO gold.fact_transactions (
    transaction_key,
    user_key,
    card_key,
    merchant_key,
    date_key,
    time_key,
    amount,
    use_chip,
    errors,
    is_fraud
)

SELECT
    st.transaction_id,
    du.user_key,
    dc.card_key,
    dm.merchant_key,
    dd.date_key,
    dt.time_key,
    st.amount,
    st.use_chip,
    st.errors,
    st.is_fraud

FROM silver.transactions st

JOIN gold.dim_users du
    ON st.user_id = du.user_id

JOIN gold.dim_cards dc
    ON st.user_id = dc.user_id
   AND st.card_index = dc.card_index

JOIN gold.dim_merchants dm
    ON st.merchant_name = dm.merchant_name
   AND st.merchant_city = dm.merchant_city
   AND st.merchant_state = dm.merchant_state
   AND st.zipcode = dm.zipcode
   AND st.mcc = dm.mcc

JOIN gold.dim_date dd
    ON st.transaction_date = dd.full_date

JOIN gold.dim_time dt
    ON st.transaction_time = dt.full_time

/*
ON CONFLICT (transaction_key)
DO UPDATE SET
    user_key     = EXCLUDED.user_key,
    card_key     = EXCLUDED.card_key,
    merchant_key = EXCLUDED.merchant_key,
    date_key     = EXCLUDED.date_key,
    time_key     = EXCLUDED.time_key,
    amount       = EXCLUDED.amount,
    use_chip     = EXCLUDED.use_chip,
    errors       = EXCLUDED.errors,
    is_fraud     = EXCLUDED.is_fraud;

    */