from sanic import Sanic

from entrypoint import bootstrap
from utils import utils

db = utils.init_database()

async def create_app(config_name="default"):
    app = Sanic(__name__)
    application = app
    application.ctx.bus = await bootstrap.bootstrap(db= db)
    application.ctx.db = db
    return application


# init_bus