from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from server.extensions import db, limiter, login, mail
from server.routes import (
    accounts,
    auth,
    devices,
    errors,
    folders,
    index,
    shares,
    user,
)
from server.utils import config, security


def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.from_mapping(**config.flask_config)

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app: Flask):
    db.init_app(app)
    limiter.init_app(app)
    login.init_app(app)
    mail.init_app(app)


def register_blueprints(app: Flask):
    app.register_blueprint(accounts.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(devices.bp)
    app.register_blueprint(errors.bp)
    app.register_blueprint(folders.bp)
    app.register_blueprint(index.bp)
    app.register_blueprint(shares.bp)
    app.register_blueprint(user.bp)
