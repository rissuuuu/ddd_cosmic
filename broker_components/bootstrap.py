from databases import Database
from settings import Settings

def init_database(settings: Settings) ->  Database:
    return Database(settings.pg_dsn,force_rollback=True)
