import sentry_sdk

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.middleware.proxy_fix import ProxyFix

from server import utils
from server.extensions import db, limiter, login, mail, metrics, redis
from server.models.device import Device
from server.models.share import Share
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
from server.utils import config, security  # noqa


def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.from_mapping(**config.flask_config)

    if app.debug is False:
        sentry_sdk.init(
            config.SENTRY_DSN,
            integrations=[FlaskIntegration()],
        )

    register_extensions(app)
    register_blueprints(app)
    register_scheduler(app)

    return app


def register_extensions(app: Flask):
    db.init_app(app)
    limiter.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    metrics.init_app(app)
    redis.init_app(app)


def register_blueprints(app: Flask):
    app.register_blueprint(accounts.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(devices.bp)
    app.register_blueprint(errors.bp)
    app.register_blueprint(folders.bp)
    app.register_blueprint(index.bp)
    app.register_blueprint(shares.bp)
    app.register_blueprint(user.bp)


def register_scheduler(app: Flask):
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        utils.with_context(app, Share.delete_expired), "interval", minutes=10
    )

    scheduler.add_job(
        utils.with_context(app, Device.delete_expired), "interval", hours=1
    )

    scheduler.start()
