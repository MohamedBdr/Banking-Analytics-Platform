
DROP TABLE IF EXISTS silver.transactions CASCADE;

CREATE TABLE IF NOT EXISTS silver.transactions (
    transaction_id             BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id                    INTEGER NOT NULL,
    card_index                 SMALLINT NOT NULL,
    transaction_date           DATE,
    transaction_time           TIME,
    amount                     NUMERIC(12,2),
    use_chip                   VARCHAR(50),
    merchant_name              VARCHAR(50),
    merchant_city              VARCHAR(50),
    merchant_state             VARCHAR(50),
    zipcode                    VARCHAR(20),
    mcc                        INTEGER,
    errors                     TEXT,
    is_fraud                   BOOLEAN

);

INSERT INTO silver.transactions (
    user_id,
    card_index,
    transaction_date,
    transaction_time,
    amount,
    use_chip,
    merchant_name,
    merchant_city,
    merchant_state,
    zipcode,
    mcc,
    errors,
    is_fraud
)

SELECT
    CAST("User" AS INTEGER),
    CAST("Card" AS SMALLINT),
        MAKE_DATE(
            CAST("Year" AS INTEGER),
            CAST("Month" AS INTEGER),
            CAST("Day" AS INTEGER)
        ),
    CAST("Time" AS TIME),
    CAST(
        REPLACE(
            REPLACE(TRIM("Amount"), '$', ''),
            ',',
            ''
        ) AS NUMERIC(12,2)
    ),
    TRIM("Use Chip"),
    TRIM("Merchant Name"),
    NULLIF(TRIM("Merchant City"), ''),
    NULLIF(TRIM("Merchant State"), ''),
    NULLIF(TRIM("Zip"), ''),
    CAST("MCC" AS INTEGER),
    NULLIF(TRIM("Errors?"), ''),
    CASE
        WHEN UPPER(TRIM("Is Fraud?")) = 'YES' THEN TRUE
        ELSE FALSE
    END
FROM bronze.transactions;

/*

ON CONFLICT (transaction_id)

DO UPDATE SET
    user_id           = EXCLUDED.user_id,
    card_index        = EXCLUDED.card_index,
    transaction_date  = EXCLUDED.transaction_date,
    transaction_time  = EXCLUDED.transaction_time,
    amount            = EXCLUDED.amount,
    use_chip          = EXCLUDED.use_chip,
    merchant_name     = EXCLUDED.merchant_name,
    merchant_city     = EXCLUDED.merchant_city,
    merchant_state    = EXCLUDED.merchant_state,
    zipcode           = EXCLUDED.zipcode,
    mcc               = EXCLUDED.mcc,
    errors            = EXCLUDED.errors,
    is_fraud          = EXCLUDED.is_fraud;
    */