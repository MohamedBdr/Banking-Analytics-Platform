from src.database.create_database import create_database
from src.database.create_schemas import create_schemas
from src.database.execute_sql import execute_sql
from src.bronze.load_bronze import load_users, load_cards, load_transactions
from src.database.connection import get_engine
from sqlalchemy import text
from src.logging.decorators import log_execution
from src.logging.logger import logger
from src.validation.runner import run_validations

from src.audit.audit import (
    start_pipeline,
    finish_pipeline,
    fail_pipeline,
    start_step,
    finish_step,
    fail_step
)


def get_row_count(table_name):
    engine = get_engine()

    with engine.connect() as conn:
        return conn.execute(
            text(f"SELECT COUNT(*) FROM {table_name}")
        ).scalar()

@log_execution
def run_sql_step(run_id, step_name, sql_file, table_name):

    logger.info(f"Executing SQL step: {step_name}")

    step_id = start_step(run_id, step_name)

    try:
        execute_sql(sql_file)

        rows = get_row_count(table_name)

        finish_step(step_id, rows)

        logger.info(f"Step '{step_name}' completed successfully ({rows} rows)")

    except Exception as e:

        fail_step(step_id, e)

        logger.exception(f"Step '{step_name}' failed")

        raise    

@log_execution
def run_bronze_step(run_id, step_name, loader, table_name):

    logger.info(f"Executing Bronze step: {step_name}")

    step_id = start_step(run_id, step_name)

    try:
        loader()

        rows = get_row_count(table_name)

        finish_step(step_id, rows)

        logger.info(f"Step '{step_name}' completed successfully ({rows} rows)")

    except Exception as e:

        fail_step(step_id, e)

        logger.exception(f"Step '{step_name}' failed")  
        raise

@log_execution
def main():
    """
        Main ETL Pipeline.
    """
    create_database()
    create_schemas()
    
    # =========================
    # Start Pipeline Audit
    # =========================
    run_id = start_pipeline("Banking Analytics Platform")

    try:

        execute_sql("sql/001_create_schema.sql")
        execute_sql("sql/002_create_audit.sql")
        execute_sql("sql/003_create_bronze_tables.sql")
        
        # =========================
        # Bronze Layer
        # =========================
        run_bronze_step(
            run_id,
            "Bronze Users",
            load_users,
            "bronze.users"
        )

        run_bronze_step(
            run_id,
            "Bronze Cards",
            load_cards,
            "bronze.cards"
        )

        run_bronze_step(
            run_id,
            "Bronze Transactions",
            load_transactions,
            "bronze.transactions"
        )

        # =========================
        # Data Validation
        # =========================
        validation_failed  = run_validations()
        if validation_failed:
            logger.error("Data validation failed. Pipeline stopped.")
            return
        
        # =========================
        # Silver Layer
        # =========================
        run_sql_step(
            run_id,
            "Silver Users",
            "sql/silver/001_users.sql",
            "silver.users"
        )

        run_sql_step(
            run_id,
            "Silver Cards",
            "sql/silver/002_cards.sql",
            "silver.cards"
        )

        run_sql_step(
            run_id,
            "Silver Transactions",
            "sql/silver/003_transactions.sql",
            "silver.transactions"
        )

        # =========================
        # Gold Layer
        # =========================
        run_sql_step(
            run_id,
            "Dim Users",
            "sql/gold/001_dim_users.sql",
            "gold.dim_users"
        )

        run_sql_step(
            run_id,
            "Dim Cards",
            "sql/gold/002_dim_cards.sql",
            "gold.dim_cards"
        )

        run_sql_step(
            run_id,
            "Dim Merchants",
            "sql/gold/003_dim_merchants.sql",
            "gold.dim_merchants"
        )

        run_sql_step(
            run_id,
            "Dim Date",
            "sql/gold/004_dim_date.sql",
            "gold.dim_date"
        )

        run_sql_step(
            run_id,
            "Dim Time",
            "sql/gold/005_dim_time.sql",
            "gold.dim_time"
        )

        run_sql_step(
            run_id,
            "Fact Transactions",
            "sql/gold/006_fact_transactions.sql",
            "gold.fact_transactions"
        )

        execute_sql("sql/004_indexes.sql")

        # =========================
        # Finish Pipeline Audit
        # =========================
        finish_pipeline(run_id)

    except Exception as e:
        fail_pipeline(run_id, e)
        raise


if __name__ == "__main__":
    main()
