class BaseConfig(object):
    APP_NAME = "ufc_fight_predictor"
    DEBUG = False
    SECRET_KEY = "SOME TEST SECRET"

    # DATABASE STUFF WILL GO HERE?


class DevConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    pass
