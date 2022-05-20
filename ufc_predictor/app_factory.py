from flask import Flask


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    from .logistic_regression import views
    app.register_blueprint(views.logistic_regresion_views)

    @app.route('/hello')
    def hello():
        return 'Hello World!'
    return app
