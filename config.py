import boto3
import json


class BaseConfig(object):
    APP_NAME = "ufc_fight_predictor"
    DEBUG = False
    SECRET_KEY = "SOME TEST SECRET"


class DevConfig(BaseConfig):
    client = boto3.client('secretsmanager', region_name='us-east-1')
    secretMap = client.get_secret_value(
        SecretId="UfcPredictorRdsSecret-extTBzicS2ON", VersionStage="AWSCURRENT")
    rdsSecret = json.loads(secretMap.get("SecretString"))
    ENVIRONMENT = "dev"
    DEBUG = True
    MYSQL_DATABASE_USER = rdsSecret.get("username")
    MYSQL_DATABASE_PASSWORD = rdsSecret.get("password")
    MYSQL_DATABASE_DB = rdsSecret.get("dbname")
    MYSQL_DATABASE_HOST = rdsSecret.get("host")


class ProductionConfig(BaseConfig):
    ENVIRONMENT = "production"
    pass
