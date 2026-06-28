
-- ============================================================
-- BRONZE.USERS
-- ============================================================

CREATE TABLE IF NOT EXISTS bronze.users (
    "Person" TEXT,
    "Current Age" TEXT,
    "Retirement Age" TEXT,
    "Birth Year" TEXT,
    "Birth Month" TEXT,
    "Gender" TEXT,
    "Address" TEXT,
    "Apartment" TEXT,
    "City" TEXT,
    "State" TEXT,
    "Zipcode" TEXT,
    "Latitude" TEXT,
    "Longitude" TEXT,
    "Per Capita Income - Zipcode" TEXT,
    "Yearly Income - Person" TEXT,
    "Total Debt" TEXT,
    "FICO Score" TEXT,
    "Num Credit Cards" TEXT,

    source_file VARCHAR(255),
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- BRONZE.CARDS
-- ============================================================

CREATE TABLE IF NOT EXISTS bronze.cards (
    "User" TEXT,
    "CARD INDEX" TEXT,
    "Card Brand" TEXT,
    "Card Type" TEXT,
    "Card Number" TEXT,
    "Expires" TEXT,
    "CVV" TEXT,
    "Has Chip" TEXT,
    "Cards Issued" TEXT,
    "Credit Limit" TEXT,
    "Acct Open Date" TEXT,
    "Year PIN last Changed" TEXT,
    "Card on Dark Web" TEXT,

    source_file VARCHAR(255),
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- BRONZE.TRANSACTIONS
-- ============================================================
DROP TABLE IF EXISTS bronze.transactions CASCADE;

CREATE TABLE IF NOT EXISTS bronze.transactions (
    "User" TEXT,
    "Card" TEXT,
    "Year" TEXT,
    "Month" TEXT,
    "Day" TEXT,
    "Time" TEXT,
    "Amount" TEXT,
    "Use Chip" TEXT,
    "Merchant Name" TEXT,
    "Merchant City" TEXT,
    "Merchant State" TEXT,
    "Zip" TEXT,
    "MCC" INTEGER,
    "Errors?" TEXT,
    "Is Fraud?" TEXT,

    source_file VARCHAR(255),
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);