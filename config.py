class BaseConfig(object):
    APP_NAME = "ufc_fight_predictor"
    DEBUG = False
    SECRET_KEY = "SOME TEST SECRET"

    # DATABASE STUFF WILL GO HERE?


class DevConfig(BaseConfig):
    DEBUG = True
    MYSQL_DATABASE_USER = 'mysqlAdmin'
    MYSQL_DATABASE_PASSWORD = 'eRJ3qmc-yl4t1QM71^3sfVEL_GuZty'
    MYSQL_DATABASE_DB = 'thisisatest'
    MYSQL_DATABASE_HOST = 'uucna2s149iknf.cdxfj1ghajls.us-east-1.rds.amazonaws.com'


class ProductionConfig(BaseConfig):
    pass
