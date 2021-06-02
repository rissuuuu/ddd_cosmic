from databases import Database

from ddd_cosmic import config


def init_database() -> Database:
    return Database(
        config.PostgresConfig().get_postgres_url()
    )


def get_bootstrap(app):
    return app.ctx.bus
