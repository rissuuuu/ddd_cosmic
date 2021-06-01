from sanic import Sanic
from databases import Database

from entrypoint import bootstrap
from ddd_cosmic import config

def init_database() -> Database:
    return Database(
        config.PostgresConfig().get_postgres_url()
    )

db = init_database()

# onstart database start and close on on_close

def create_app(config_name="default"):
    app = Sanic(__name__)
    application = app
    application.ctx.bus = bootstrap.bootstrap(db= db)
    application.ctx.db = db
    return application


# init_bus