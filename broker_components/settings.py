from pydantic import BaseModel, PostgresDsn, RedisDsn


class Settings(BaseModel):
    pg_dsn : PostgresDsn
    redis_settings : RedisDsn

class AppSettings(Settings):
    pg_dsn : PostgresDsn = "postgresql://admin:localhost@localhost:5432/floorsheet"
    redis_settings :RedisDsn = "redis://localhost:6379/0"
