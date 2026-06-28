-- DROP TABLE IF EXISTS gold.dim_users CASCADE;

CREATE TABLE IF NOT EXISTS gold.dim_users (
    user_key                    INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id                     INTEGER UNIQUE NOT NULL,
    person                      VARCHAR(50),
    current_age                 SMALLINT,
    retirement_age              SMALLINT,
    birth_year                  SMALLINT,
    birth_month                 SMALLINT,
    gender                      VARCHAR(10),
    address                     TEXT,
    apartment                   TEXT,
    city                        VARCHAR(100),
    state                       VARCHAR(50),
    zipcode                     VARCHAR(20),
    latitude                    NUMERIC(10,6),
    longitude                   NUMERIC(10,6),
    per_capita_income_zipcode   INTEGER,
    yearly_income_person        INTEGER,
    total_debt                  INTEGER,
    fico_score                  SMALLINT,
    num_credit_cards            SMALLINT
);

INSERT INTO gold.dim_users (
    user_id,
    person,
    current_age,
    retirement_age,
    birth_year,
    birth_month,
    gender,
    address,
    apartment,
    city,
    state,
    zipcode,
    latitude,
    longitude,
    per_capita_income_zipcode,
    yearly_income_person,
    total_debt,
    fico_score,
    num_credit_cards
)
SELECT
    user_id,
    person,
    current_age,
    retirement_age,
    birth_year,
    birth_month,
    gender,
    address,
    apartment,
    city,
    state,
    zipcode,
    latitude,
    longitude,
    per_capita_income_zipcode,
    yearly_income_person,
    total_debt,
    fico_score,
    num_credit_cards
FROM silver.users

ON CONFLICT (user_id)

DO UPDATE SET
    person                     = EXCLUDED.person,
    current_age                = EXCLUDED.current_age,
    retirement_age             = EXCLUDED.retirement_age,
    birth_year                 = EXCLUDED.birth_year,
    birth_month                = EXCLUDED.birth_month,
    gender                     = EXCLUDED.gender,
    address                    = EXCLUDED.address,
    apartment                  = EXCLUDED.apartment,
    city                       = EXCLUDED.city,
    state                      = EXCLUDED.state,
    zipcode                    = EXCLUDED.zipcode,
    latitude                   = EXCLUDED.latitude,
    longitude                  = EXCLUDED.longitude,
    per_capita_income_zipcode  = EXCLUDED.per_capita_income_zipcode,
    yearly_income_person       = EXCLUDED.yearly_income_person,
    total_debt                 = EXCLUDED.total_debt,
    fico_score                 = EXCLUDED.fico_score,
    num_credit_cards           = EXCLUDED.num_credit_cards;