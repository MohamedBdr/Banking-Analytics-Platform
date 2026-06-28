from pathlib import Path
from sqlalchemy import text
from src.database.connection import get_engine

DATA_PATH = Path("data/raw")

def is_file_loaded(table_name, file_name):
    engine = get_engine()
    
    with engine.begin() as conn:
        result = conn.execute(
            text(f"""
                SELECT EXISTS (
                    SELECT 1
                    FROM {table_name}
                    WHERE source_file = :file_name
                )
            """),
            {"file_name": file_name},
        )

        return result.scalar()

def load_table(table_name, file_name, columns):

    engine = get_engine()

    if is_file_loaded(table_name, file_name):
        print(f"⏩ {file_name} already loaded. Skipping...")
        return

    file_path = DATA_PATH / file_name

    columns_sql = ", ".join(f'"{col}"' for col in columns)

    copy_sql = f"""
        COPY {table_name} ({columns_sql})
        FROM STDIN
        WITH (
            FORMAT CSV,
            HEADER TRUE
        )
    """

    conn = engine.raw_connection()

    try:
        cursor = conn.cursor()

        with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
            cursor.copy_expert(copy_sql, file)

        cursor.execute(
            f"""
            UPDATE {table_name}
            SET source_file = %s
            WHERE source_file IS NULL
            """,
            (file_name,)
        )

        conn.commit()
        print(f"✅ Loaded {file_name}")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error loading {file_name}")
        print(e)

    finally:
        cursor.close()
        conn.close()

def load_users():

    load_table(
        table_name="bronze.users",
        file_name="sd254_users.csv",
        columns=[
            "Person",
            "Current Age",
            "Retirement Age",
            "Birth Year",
            "Birth Month",
            "Gender",
            "Address",
            "Apartment",
            "City",
            "State",
            "Zipcode",
            "Latitude",
            "Longitude",
            "Per Capita Income - Zipcode",
            "Yearly Income - Person",
            "Total Debt",
            "FICO Score",
            "Num Credit Cards",
        ],
    )


def load_cards():

    load_table(
        table_name="bronze.cards",
        file_name="sd254_cards.csv",
        columns=[
            "User",
            "CARD INDEX",
            "Card Brand",
            "Card Type",
            "Card Number",
            "Expires",
            "CVV",
            "Has Chip",
            "Cards Issued",
            "Credit Limit",
            "Acct Open Date",
            "Year PIN last Changed",
            "Card on Dark Web",
        ],
    )
    
    
def load_transactions():
    load_table(
        table_name="bronze.transactions",
        file_name="User0_credit_card_transactions.csv",
        columns=[
            "User",
            "Card",
            "Year",
            "Month",
            "Day",
            "Time",
            "Amount",
            "Use Chip",
            "Merchant Name",
            "Merchant City",
            "Merchant State",
            "Zip",
            "MCC",
            "Errors?",
            "Is Fraud?",
        ],
    )

def load_bronze():
    load_users()
    load_cards()
    load_transactions()

if __name__ == "__main__":

    load_bronze()