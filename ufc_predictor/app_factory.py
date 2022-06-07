from flask import Flask
from ufc_predictor.extensions import mysql
from ufc_predictor.util import construct_fight_dataframe, construct_future_fight_dataframe
import pandas as pd


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    mysql.init_app(app)
    create_past_matchups_table(mysql.connect())
    create_future_matchups_table(mysql.connect())

    from .logistic_regression import views
    app.register_blueprint(views.logistic_regresion_views)

    @app.route('/hello')
    def hello():
        return 'Hello World!'
    return app


def create_past_matchups_table(conn):
    # THIS IS A TEMP SOLUTION - NEED TO CONVERT THIS STEP TO A LAMBDA MAYBE??
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
            bsapm FLOAT,
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

    # if the DB is empty, then populate it
    if cursor.fetchone()[0] == 0:
        cursor.execute("SELECT * FROM fights")
        fight_df = pd.DataFrame(cursor.fetchall()).loc[:, 1:]
        cursor.execute("SELECT * FROM fighters")
        fighter_stats = pd.DataFrame(
            cursor.fetchall()).loc[:, 1:].set_index(1).T.to_dict('list')
        past_matchup_df = construct_fight_dataframe(
            fight_df, fighter_stats, True)
        past_matchup_tuples = list(
            past_matchup_df.itertuples(index=False, name=None))
        sql = """
            INSERT INTO past_matchups (rf,bf,winner,rwins,bwins,rloses,bloses,rslpm,bslpm,rstrac,bstrac,rsapm,bsapm,rstrd,bstrd,rtdav,btdav,rtdac,btdac,rtdd,btdd,rsubav,bsubav)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
        cursor.executemany(sql, past_matchup_tuples)
        conn.commit()
    cursor.close()


def create_future_matchups_table(conn):
    # THIS IS A TEMP SOLUTION - NEED TO CONVERT THIS STEP TO A LAMBDA MAYBE??
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE if not exists future_matchups(id INT AUTO_INCREMENT PRIMARY KEY,
            date_ TEXT,
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
            bsapm FLOAT,
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

    sql = "SELECT COUNT(*) as row_count FROM future_matchups"

    cursor.execute(sql)

    # if the DB is empty, then populate it
    if cursor.fetchone()[0] == 0:
        cursor.execute("SELECT * FROM future_fights")
        future_fight_df = pd.DataFrame(cursor.fetchall()).loc[:, 1:]
        cursor.execute("SELECT * FROM fighters")
        fighter_stats = pd.DataFrame(
            cursor.fetchall()).loc[:, 1:].set_index(1).T.to_dict('list')
        future_matchup_df = construct_future_fight_dataframe(
            future_fight_df, fighter_stats)
        future_matchup_list = list(
            future_matchup_df.itertuples(index=False, name=None))
        sql = """
            INSERT INTO future_matchups (date_,rf,bf,rwins,bwins,rloses,bloses,rslpm,bslpm,rstrac,bstrac,rsapm,bsapm,rstrd,bstrd,rtdav,btdav,rtdac,btdac,rtdd,btdd,rsubav,bsubav)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
        cursor.executemany(sql, future_matchup_list)
        conn.commit()

    cursor.close()
