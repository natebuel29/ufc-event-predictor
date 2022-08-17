#from pytz import utc
from flask import Flask
#from apscheduler.schedulers.background import BackgroundScheduler
from ufc_predictor import db, util
from logging.config import dictConfig


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
    db.mysql.init_app(app)
    # TODO: delete these two functions after the db migration
    db.create_past_matchups_table(db.mysql.connect())
    db.create_future_matchups_table(db.mysql.connect())

    from .machine_learning import views as machine_learning
    app.register_blueprint(machine_learning.machine_learning_views)

    from .invalid_event import views as invalid_event
    app.register_blueprint(invalid_event.invalid_event_views)

    from .api import api
    app.register_blueprint(api.api_views)

    util.fit_ml_models()
    # Schedule the refitting of ML models once a day
    # scheduler = BackgroundScheduler()
    # scheduler.configure(timezone=utc)
    # scheduler.add_job(fit_ml_models, 'interval', hours=24,
    #                   id="fit_models")
    # scheduler.start()

    return app
