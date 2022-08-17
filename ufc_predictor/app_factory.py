from pytz import utc
from flask import Flask
#from apscheduler.schedulers.background import BackgroundScheduler
from ufc_predictor import db, ml_models, util
from logging.config import dictConfig
import logging


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

    # Schedule the refitting of ML models once a day
    fit_ml_models()
    # scheduler = BackgroundScheduler()
    # scheduler.configure(timezone=utc)
    # scheduler.add_job(fit_ml_models, 'interval', hours=24,
    #                   id="fit_models")
    # scheduler.start()

    return app


def fit_ml_models():
    logging.info("Refitting the ML models")
    fights_df = db.get_past_matchups()
    X, y = util.genererate_inputs_n_labels(fights_df)
    ml_models.log_reg_clf.fit(X, y)
    X = util.add_bias(X)
    ml_models.svm_clf.fit(X, y)
