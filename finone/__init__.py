import os

from config import common

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api
from finone.models import db

def create_app(db, config_name):
    _app = Flask(__name__)
    _app.config.from_object(config_name)
    db.init_app(_app)

    with _app.app_context():
        db.create_all()

    return _app

app = create_app(db, common)
migrate = Migrate(app, db)
marshmallow = Marshmallow(app)
api = Api(app)

if app.debug:
    from flask_debugtoolbar import DebugToolbarExtension

    toolbar = DebugToolbarExtension(app)

from finone import routes
