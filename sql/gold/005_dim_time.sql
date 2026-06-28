-- DROP TABLE IF EXISTS gold.dim_time CASCADE;

CREATE TABLE IF NOT EXISTS gold.dim_time (
    time_key        INTEGER PRIMARY KEY,
    full_time       TIME NOT NULL UNIQUE,
    hour            SMALLINT,
    minute          SMALLINT,
    second          SMALLINT,
    am_pm           VARCHAR(2),
    time_of_day     VARCHAR(20)
);

INSERT INTO gold.dim_time (
    time_key,
    full_time,
    hour,
    minute,
    second,
    am_pm,
    time_of_day
)

SELECT
    CAST(TO_CHAR(transaction_time, 'HH24MI') AS INTEGER),
    transaction_time,
    EXTRACT(HOUR FROM transaction_time),
    EXTRACT(MINUTE FROM transaction_time),
    EXTRACT(SECOND FROM transaction_time),
    TO_CHAR(transaction_time, 'AM'),
    CASE
        WHEN EXTRACT(HOUR FROM transaction_time) BETWEEN 0 AND 5 THEN 'Night'
        WHEN EXTRACT(HOUR FROM transaction_time) BETWEEN 6 AND 11 THEN 'Morning'
        WHEN EXTRACT(HOUR FROM transaction_time) BETWEEN 12 AND 17 THEN 'Afternoon'
        ELSE 'Evening'
    END

FROM (
    SELECT DISTINCT transaction_time
    FROM silver.transactions
) t
ORDER BY transaction_time

ON CONFLICT (time_key)

DO UPDATE SET
    full_time   = EXCLUDED.full_time,
    hour        = EXCLUDED.hour,
    minute      = EXCLUDED.minute,
    second      = EXCLUDED.second,
    am_pm       = EXCLUDED.am_pm,
    time_of_day = EXCLUDED.time_of_day;