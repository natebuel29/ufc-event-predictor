from flask import Flask
from ufc_predictor.database.database_connector import MySqlDatabaseConnection


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db_connect = MySqlDatabaseConnection(host="uucna2s149iknf.cdxfj1ghajls.us-east-1.rds.amazonaws.com",
                                         database="thisisatest",
                                         password="eRJ3qmc-yl4t1QM71^3sfVEL_GuZty",
                                         user="mysqlAdmin")

    from .logistic_regression import views
    app.register_blueprint(views.logistic_regresion_views)

    @app.route('/hello')
    def hello():
        return 'Hello World!'
    return app
