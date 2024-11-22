from flask import Flask

def create_app() -> Flask:
    app = Flask(__name__)
    app.debug = True

    # import route.py and register to blueprint
    from . import routes
    app.register_blueprint(routes.bp)

    return app