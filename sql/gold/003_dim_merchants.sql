DROP TABLE IF EXISTS gold.dim_merchants CASCADE;

CREATE TABLE IF NOT EXISTS gold.dim_merchants (
    merchant_key      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    merchant_name     VARCHAR(50),
    merchant_city     VARCHAR(50),
    merchant_state    VARCHAR(50),
    zipcode           VARCHAR(20),
    mcc               INTEGER
);

INSERT INTO gold.dim_merchants (
    merchant_name,
    merchant_city,
    merchant_state,
    zipcode,
    mcc
)

SELECT DISTINCT
    merchant_name,
    merchant_city,
    merchant_state,
    zipcode,
    mcc
FROM silver.transactions
/*
ON CONFLICT (
    merchant_name,
    merchant_city,
    merchant_state,
    zipcode,
    mcc
)
DO UPDATE SET
    merchant_city  = EXCLUDED.merchant_city,
    merchant_state = EXCLUDED.merchant_state,
    zipcode        = EXCLUDED.zipcode,
    mcc            = EXCLUDED.mcc;
*/