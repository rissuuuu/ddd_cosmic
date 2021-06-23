import os
from databases import Database
# from dotenv import load_dotenv
#
# load_dotenv()


def get_postgres_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", 5432)
    password = os.environ.get("DB_PASSWORD", "localhost")
    user = os.environ.get("POSTGRES_USER", "admin")
    db_name = os.environ.get("DB_NAME", "company")

    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def init_db():
    url = get_postgres_uri()
    return Database(url)
