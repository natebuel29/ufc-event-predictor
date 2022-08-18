#from pytz import utc
from flask import Flask
#from apscheduler.schedulers.background import BackgroundScheduler
from ufc_predictor import db, util, auth
from logging.config import dictConfig
import boto3
import json


def create_app(config_object):
    # config for the logger
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })

    app = Flask(__name__)
    app.logger.info(
        f"Creating ufc-event-predictor app for {config_object.ENVIRONMENT} env")
    app.config.from_object(config_object)

    # setup basic auth for api
    client = boto3.client('secretsmanager', region_name='us-east-1')
    secretMap = client.get_secret_value(
        SecretId="UfcEventPredictorApiSecret0-Z6TyTAY1hN5n", VersionStage="AWSCURRENT")
    api_key = secretMap.get("SecretString")

    app.config['BASIC_AUTH_USERNAME'] = "api_user"
    app.config['BASIC_AUTH_PASSWORD'] = api_key
    auth.basic_auth.init_app(app)

    # init DB stuff
    db.mysql.init_app(app)
    # TODO: delete these two functions after the db migration
    db.create_past_matchups_table(db.mysql.connect())
    db.create_future_matchups_table(db.mysql.connect())

    util.fit_ml_models()

    from .machine_learning import views as machine_learning
    app.register_blueprint(machine_learning.machine_learning_views)

    from .invalid_event import views as invalid_event
    app.register_blueprint(invalid_event.invalid_event_views)

    from .api import api
    app.register_blueprint(api.api_views)

    return app
