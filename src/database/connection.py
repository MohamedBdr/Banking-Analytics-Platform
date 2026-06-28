from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv('POSTGRES_DATABASE_NAME')

def get_engine(db_name=DB_NAME):
    url = (
        f"postgresql+psycopg2://"
        f"{os.getenv('POSTGRES_CONN_USERNAME')}:"
        f"{os.getenv('POSTGRES_CONN_PASSWORD')}@"
        f"{os.getenv('POSTGRES_CONN_HOST')}:"
        f"{os.getenv('POSTGRES_CONN_PORT')}/"
        f"{db_name}"
    )
    return create_engine(url)