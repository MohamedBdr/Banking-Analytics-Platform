
-- DROP TABLE IF EXISTS gold.dim_date CASCADE;

CREATE TABLE IF NOT EXISTS gold.dim_date (
    date_key        INTEGER PRIMARY KEY,
    full_date       DATE NOT NULL UNIQUE,
    day             SMALLINT,
    month           SMALLINT,
    month_name      VARCHAR(20),
    quarter         SMALLINT,
    year            SMALLINT,
    day_of_week     SMALLINT,
    day_name        VARCHAR(20),
    week_of_year    SMALLINT,
    is_weekend      BOOLEAN
);

INSERT INTO gold.dim_date (
    date_key,
    full_date,
    day,
    month,
    month_name,
    quarter,
    year,
    day_of_week,
    day_name,
    week_of_year,
    is_weekend
)
SELECT
    TO_CHAR(transaction_date, 'YYYYMMDD')::INTEGER,
    transaction_date,
    EXTRACT(DAY FROM transaction_date),
    EXTRACT(MONTH FROM transaction_date),
    TO_CHAR(transaction_date, 'Month'),
    EXTRACT(QUARTER FROM transaction_date),
    EXTRACT(YEAR FROM transaction_date),
    EXTRACT(ISODOW FROM transaction_date),
    TO_CHAR(transaction_date, 'Day'),
    EXTRACT(WEEK FROM transaction_date),
    CASE
        WHEN EXTRACT(ISODOW FROM transaction_date) IN (6,7) THEN TRUE
        ELSE FALSE
    END
FROM (
    SELECT DISTINCT transaction_date
    FROM silver.transactions
) d
ORDER BY transaction_date

ON CONFLICT (date_key)

DO UPDATE SET
    full_date    = EXCLUDED.full_date,
    day          = EXCLUDED.day,
    month        = EXCLUDED.month,
    month_name   = EXCLUDED.month_name,
    quarter      = EXCLUDED.quarter,
    year         = EXCLUDED.year,
    day_of_week  = EXCLUDED.day_of_week,
    day_name     = EXCLUDED.day_name,
    week_of_year = EXCLUDED.week_of_year,
    is_weekend   = EXCLUDED.is_weekend;
