##connect to db
import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    required_vars = ["DB_NAME", "DB_USER", "DB_PASSWORD"]
    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        raise EnvironmentError(
            f"Missing database environment variables: {', '.join(missing)}"
        )

    return psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
    )