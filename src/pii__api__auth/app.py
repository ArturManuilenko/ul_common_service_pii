from flask import Flask
from flask_migrate import Migrate
from db_utils.modules.db import db
from db_utils.modules.db import attach_to_flask_app
from src.conf.pii__api__auth import API__VERSION
from src.conf.pii__db__general import db_config


migrate = Migrate()


app = Flask(__name__)
app.config.from_object('src.conf.api.Config')
attach_to_flask_app(app, db_config)
migrate.init_app(app, db)

# import here because of api routes need init db in attach_to_app method
from src.pii__api__auth.routes import api_bp          # noqa: F401
app.register_blueprint(api_bp, url_prefix=f'/api/{API__VERSION}/')

__all__ = (
    "app",
    "db",
)
