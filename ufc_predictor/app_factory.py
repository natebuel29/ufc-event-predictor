from flask import Flask
from ufc_predictor import db


def create_app(config_object):
    # TODO: Add logs
    app = Flask(__name__)
    app.config.from_object(config_object)
    db.mysql.init_app(app)
    db.create_past_matchups_table(db.mysql.connect())
    db.create_future_matchups_table(db.mysql.connect())

    from .logistic_regression import views as logistic_regression
    app.register_blueprint(logistic_regression.logistic_regresion_views)

    from .invalid_event import views as invalid_event
    app.register_blueprint(invalid_event.invalid_event_views)

    return app
