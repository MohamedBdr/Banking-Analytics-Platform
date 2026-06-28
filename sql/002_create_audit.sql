CREATE TABLE IF NOT EXISTS audit.etl_runs (
    run_id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    pipeline_name       VARCHAR(100) NOT NULL,
    start_time          TIMESTAMP NOT NULL,
    end_time            TIMESTAMP,
    duration_seconds    NUMERIC(10,2),
    status              VARCHAR(20),
    error_message       TEXT
);

------------------------------------------------

CREATE TABLE IF NOT EXISTS audit.etl_steps (

    step_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    run_id BIGINT NOT NULL
        REFERENCES audit.etl_runs(run_id),

    step_name VARCHAR(100) NOT NULL,

    start_time TIMESTAMP NOT NULL,

    end_time TIMESTAMP,

    duration_seconds NUMERIC(10,2),

    rows_loaded BIGINT,

    status VARCHAR(20) NOT NULL,

    error_message TEXT
);

--------------------------------------------
CREATE TABLE IF NOT EXISTS audit.rejected_transactions (

    rejected_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    user_id TEXT,
    card_index TEXT,

    transaction_date TEXT,
    transaction_time TEXT,

    amount TEXT,

    merchant_name TEXT,

    reject_reason TEXT,

    rejected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);