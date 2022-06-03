from flask import Flask
from flaskext.mysql import MySQL
from ufc_predictor.util import construct_fight_dataframe
import pandas as pd


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    mysql = MySQL()
    mysql.init_app(app)
    create_past_matchups_table(mysql.connect())

    from .logistic_regression import views
    app.register_blueprint(views.logistic_regresion_views)

    @app.route('/hello')
    def hello():
        return 'Hello World!'
    return app


def create_past_matchups_table(conn):
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE if not exists past_matchups(id INT AUTO_INCREMENT PRIMARY KEY,
            rf TEXT,
            bf TEXT,
            winner INT,
            rwins INT,
            bwins INT,
            rloses INT,
            bloses INT,
            rslpm FLOAT,
            bslpm FLOAT,
            rstrac FLOAT,
            bstrac FLOAT,
            rsapm FLOAT,
            rstrd FLOAT,
            bstrd FLOAT,
            rtdav FLOAT,
            btdav FLOAT,
            rtdac FLOAT,
            btdac FLOAT,
            rtdd FLOAT,
            btdd FLOAT,
            rsubav FLOAT,
            bsubav FLOAT)"""
    )

    sql = "SELECT COUNT(*) as row_count FROM past_matchups"

    cursor.execute(sql)

    if cursor.fetchone()[0] == 0:
        cursor.execute("SELECT * FROM fights")
        fight_df = pd.DataFrame(cursor.fetchall()).loc[:, 1:]
        print(cursor.fetchall())
        print(fight_df)
        cursor.execute("SELECT * FROM fighters")
        fighter_stats = pd.DataFrame(
            cursor.fetchall()).loc[:, 1:].set_index(1).T.to_dict('list')
        print(construct_fight_dataframe(fight_df, fighter_stats, True))
    cursor.close()


def create_future_matchups_table(conn):
    cursor = cursor()
    cursor.execute(
        """CREATE TABLE if not exists future_matchups(id INT AUTO_INCREMENT PRIMARY KEY,
            rf TEXT,
            bf TEXT,
            rwins INT,
            bwins INT,
            rloses INT,
            bloses INT,
            rslpm FLOAT,
            bslpm FLOAT,
            rstrac FLOAT,
            bstrac FLOAT,
            rsapm FLOAT,
            rstrd FLOAT,
            bstrd FLOAT,
            rtdav FLOAT,
            btdav FLOAT,
            rtdac FLOAT,
            btdac FLOAT,
            rtdd FLOAT,
            btdd FLOAT,
            rsubav FLOAT,
            bsubav FLOAT)"""
    )
