from sanic import Sanic

from entrypoint import bootstrap
from utils import utils

db = utils.init_database()

def create_app(config_name="default"):
    app = Sanic(__name__)
    application = app
    application.ctx.bus = bootstrap.bootstrap(db= db)
    application.ctx.db = db
    return application


# init_bus