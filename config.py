class BaseConfig(object):
    APP_NAME = "ufc_fight_predictor"
    DEBUG = False
    SECRET_KEY = "SOME TEST SECRET"

    # DATABASE STUFF WILL GO HERE?


class DevConfig(BaseConfig):
    DEBUG = True
    MYSQL_DATABASE_USER = 'mysqlAdmin'
    MYSQL_DATABASE_PASSWORD = ''
    MYSQL_DATABASE_DB = 'thisisatest'
    MYSQL_DATABASE_HOST = ''


class ProductionConfig(BaseConfig):
    pass
