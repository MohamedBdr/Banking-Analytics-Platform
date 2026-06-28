-- DROP TABLE IF EXISTS silver.users CASCADE;

CREATE TABLE IF NOT EXISTS silver.users (
    user_id                    INTEGER PRIMARY KEY,
    person                     VARCHAR(50),
    current_age                SMALLINT,
    retirement_age             SMALLINT,
    birth_year                 SMALLINT,
    birth_month                SMALLINT,
    gender                     VARCHAR(10),
    address                    TEXT,
    apartment                  TEXT,
    city                       VARCHAR(100),
    state                      VARCHAR(50),
    zipcode                    VARCHAR(20),
    latitude                   NUMERIC(10,6),
    longitude                  NUMERIC(10,6),
    per_capita_income_zipcode  INTEGER,
    yearly_income_person       INTEGER,
    total_debt                 INTEGER,
    fico_score                 SMALLINT,
    num_credit_cards           SMALLINT
);


INSERT INTO silver.users (
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
    ROW_NUMBER() OVER () - 1,
    TRIM("Person"),
    CAST("Current Age" AS SMALLINT),
    CAST("Retirement Age" AS SMALLINT),
    CAST("Birth Year" AS SMALLINT),
    CAST("Birth Month" AS SMALLINT),
    TRIM("Gender"),
    TRIM("Address"),
    NULLIF(TRIM("Apartment"), ''),
    TRIM("City"),
    TRIM("State"),
    TRIM("Zipcode"),
    CAST("Latitude" AS NUMERIC(10,6)),
    CAST("Longitude" AS NUMERIC(10,6)),
    CAST(REPLACE(REPLACE("Per Capita Income - Zipcode",'$',''),',','') AS INTEGER),
    CAST(REPLACE(REPLACE("Yearly Income - Person",'$',''),',','') AS INTEGER),
    CAST(REPLACE(REPLACE("Total Debt",'$',''),',','') AS INTEGER),
    CAST("FICO Score" AS SMALLINT),
    CAST("Num Credit Cards" AS SMALLINT)
FROM bronze.users

ON CONFLICT (user_id)

DO UPDATE SET
    person = EXCLUDED.person,
    current_age = EXCLUDED.current_age,
    retirement_age = EXCLUDED.retirement_age,
    birth_year = EXCLUDED.birth_year,
    birth_month = EXCLUDED.birth_month,
    gender = EXCLUDED.gender,
    address = EXCLUDED.address,
    apartment = EXCLUDED.apartment,
    city = EXCLUDED.city,
    state = EXCLUDED.state,
    zipcode = EXCLUDED.zipcode,
    latitude = EXCLUDED.latitude,
    longitude = EXCLUDED.longitude,
    per_capita_income_zipcode = EXCLUDED.per_capita_income_zipcode,
    yearly_income_person = EXCLUDED.yearly_income_person,
    total_debt = EXCLUDED.total_debt,
    fico_score = EXCLUDED.fico_score,
    num_credit_cards = EXCLUDED.num_credit_cards;