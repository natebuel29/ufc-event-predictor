class BaseConfig(object):
    APP_NAME = "ufc_fight_predictor"
    DEBUG = False
    SECRET_KEY = "SOME TEST SECRET"

    # DATABASE STUFF WILL GO HERE?


class DevConfig(BaseConfig):
    DEBUG = True
    MYSQL_DATABASE_USER = 'mysqlAdmin'
    MYSQL_DATABASE_PASSWORD = '5bc,cx^h=H8KbdN3x.mSd95jMmZmwK'
    MYSQL_DATABASE_DB = 'thisisatest'
    MYSQL_DATABASE_HOST = 'uu1744jdr5e80dc.cdxfj1ghajls.us-east-1.rds.amazonaws.com'


class ProductionConfig(BaseConfig):
    pass
