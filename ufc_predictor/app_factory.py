from flask import Flask
from ufc_predictor import db


def create_app(config_object):
    # TODO: Add logs
    app = Flask(__name__)
    app.config.from_object(config_object)
    db.mysql.init_app(app)
    db.create_past_matchups_table(db.mysql.connect())
    db.create_future_matchups_table(db.mysql.connect())

    from .logistic_regression import views
    app.register_blueprint(views.logistic_regresion_views)

    return app
