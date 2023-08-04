from flask import Flask
from flask_migrate import Migrate
from db_utils.modules.db import db
from db_utils.modules.db import attach_to_flask_app
from src.conf.pii__db__general import db_config
import src.pii__db__general.models as models

app = Flask(__name__)

attach_to_flask_app(app, db_config)

migrate = Migrate(compare_type=True)
migrate.init_app(app, db)

__all__ = (
    'models',
    'app',
    'db',
)
