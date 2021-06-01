from sanic import Sanic


from entrypoint import bootstrap


# create engine here and pass to boottrap

# onstart database start and close on on_close

def create_app(config_name="default"):
    app = Sanic(__name__)
    application = app
    application.ctx.bus = bootstrap.bootstrap()

    application.ctx.db = bootstrap.init_database()
    return application


# init_bus