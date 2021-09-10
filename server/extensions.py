from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_mail import Mail
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics

db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)
login = LoginManager()
mail = Mail()
metrics = PrometheusMetrics.for_app_factory()
redis = FlaskRedis(decode_responses=True)
