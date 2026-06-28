-- DROP TABLE IF EXISTS silver.cards CASCADE;

CREATE TABLE IF NOT EXISTS silver.cards (
    card_id                  INTEGER GENERATED ALWAYS AS IDENTITY ( MINVALUE 0 START WITH 0 INCREMENT BY 1) PRIMARY KEY,
    user_id                  INTEGER NOT NULL,
    card_index               SMALLINT,
    card_brand               VARCHAR(50),
    card_type                VARCHAR(50),
    card_number              VARCHAR(25),
    expire_date                  DATE,
    cvv                      VARCHAR(4),
    has_chip                 BOOLEAN,
    cards_issued             SMALLINT,
    credit_limit             NUMERIC(12,2),
    acct_open_date           DATE,
    year_pin_last_changed    SMALLINT,
    card_on_dark_web         BOOLEAN,

    CONSTRAINT uq_cards UNIQUE (user_id, card_index)

);


INSERT INTO silver.cards (
    user_id,
    card_index,
    card_brand,
    card_type,
    card_number,
    expire_date,
    cvv,
    has_chip,
    cards_issued,
    credit_limit,
    acct_open_date,
    year_pin_last_changed,
    card_on_dark_web
)

SELECT
    CAST("User" AS INTEGER),
    CAST("CARD INDEX" AS SMALLINT),
    TRIM("Card Brand"),
    TRIM("Card Type"),
    TRIM("Card Number"),
    TO_DATE('01/' || TRIM("Expires"), 'DD/MM/YYYY'),
    TRIM("CVV"),
    CASE
        WHEN TRIM("Has Chip") = 'YES' THEN TRUE
        ELSE FALSE
    END,
    CAST("Cards Issued" AS SMALLINT),
    CAST(
        REPLACE(
            REPLACE("Credit Limit", '$', ''),
            ',',''
        ) AS NUMERIC(12,2)
    ),
    TO_DATE(TRIM("Acct Open Date"), 'MM/YYYY'),
    CAST("Year PIN last Changed" AS SMALLINT),
    CASE
        WHEN UPPER(TRIM("Card on Dark Web")) = 'YES' THEN TRUE
        ELSE FALSE
    END
FROM bronze.cards
ORDER BY
    CAST("User" AS INTEGER),
    CAST("CARD INDEX" AS INTEGER)

ON CONFLICT (user_id, card_index)

DO UPDATE SET
    card_brand = EXCLUDED.card_brand,
    card_type = EXCLUDED.card_type,
    card_number = EXCLUDED.card_number,
    expire_date = EXCLUDED.expire_date,
    cvv = EXCLUDED.cvv,
    has_chip = EXCLUDED.has_chip,
    cards_issued = EXCLUDED.cards_issued,
    credit_limit = EXCLUDED.credit_limit,
    acct_open_date = EXCLUDED.acct_open_date,
    year_pin_last_changed = EXCLUDED.year_pin_last_changed,
    card_on_dark_web = EXCLUDED.card_on_dark_web;