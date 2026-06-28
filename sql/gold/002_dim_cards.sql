-- DROP TABLE IF EXISTS gold.dim_cards CASCADE;

CREATE TABLE IF NOT EXISTS gold.dim_cards (
    card_key                  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    card_id                   INTEGER UNIQUE NOT NULL,
    user_id                   INTEGER NOT NULL,
    card_index                SMALLINT,
    card_brand                VARCHAR(50),
    card_type                 VARCHAR(50),
    card_number               VARCHAR(25),
    expire_date               DATE,
    cvv                       VARCHAR(4),
    has_chip                  BOOLEAN,
    cards_issued              SMALLINT,
    credit_limit              NUMERIC(12,2),
    acct_open_date            DATE,
    year_pin_last_changed     SMALLINT,
    card_on_dark_web          BOOLEAN
);

INSERT INTO gold.dim_cards (
    card_id,
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
    card_id,
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
FROM silver.cards

ON CONFLICT (card_id)

DO UPDATE SET
    user_id               = EXCLUDED.user_id,
    card_index            = EXCLUDED.card_index,
    card_brand            = EXCLUDED.card_brand,
    card_type             = EXCLUDED.card_type,
    card_number           = EXCLUDED.card_number,
    expire_date           = EXCLUDED.expire_date,
    cvv                   = EXCLUDED.cvv,
    has_chip              = EXCLUDED.has_chip,
    cards_issued          = EXCLUDED.cards_issued,
    credit_limit          = EXCLUDED.credit_limit,
    acct_open_date        = EXCLUDED.acct_open_date,
    year_pin_last_changed = EXCLUDED.year_pin_last_changed,
    card_on_dark_web      = EXCLUDED.card_on_dark_web;
