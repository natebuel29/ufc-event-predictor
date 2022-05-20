import os
from ufc_predictor.app_factory import create_app
import config

if os.environ['FLASK_ENV'] == 'production':
    app = create_app(config.ProductionConfig)
else:
    app = create_app(config.DevConfig)
