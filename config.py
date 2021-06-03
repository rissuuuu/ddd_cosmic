import os


class Config:
    DEBUG = os.environ.get("DEBUG", True)
    ENV = os.environ.get("ENV", "development")
    DATABASE_HOST = os.environ.get("DATABASE_HOST", "localhost")
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "floorsheet")
    DATABASE_USER = os.environ.get("DATABASE_USER", "admin")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "localhost")
    DATABASE_PORT = os.environ.get("DATABASE_PORT", 5432)
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", True)
    DATABASE_CONNECT_OPTIONS = {}


class PostgresConfig(Config):
    def get_postgres_url(self):
        SQLALCHEMY_DATABASE_URI = f"postgresql://{Config.DATABASE_USER}:{Config.DATABASE_PASSWORD}@{Config.DATABASE_HOST}:{Config.DATABASE_PORT}/{Config.DATABASE_NAME}"
        return SQLALCHEMY_DATABASE_URI
