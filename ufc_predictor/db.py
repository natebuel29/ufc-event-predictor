from flaskext.mysql import MySQL
from ufc_predictor.util import construct_fight_dataframe, construct_future_fight_dataframe
import pandas as pd
import logging

mysql = MySQL()


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
            event_name TEXT,
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
            INSERT INTO future_matchups (date_,event_name,rf,bf,rwins,bwins,rloses,bloses,rslpm,bslpm,rstrac,bstrac,rsapm,bsapm,rstrd,bstrd,rtdav,btdav,rtdac,btdac,rtdd,btdd,rsubav,bsubav)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
        cursor.executemany(sql, future_matchup_list)
        conn.commit()

    cursor.close()


def get_future_machups(date):
    logging.info(f"Grabbing future UFC fights from database for {date}")
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM future_matchups WHERE date_='{date}'")
    future_df = pd.DataFrame(cursor.fetchall())
    if len(future_df) > 0:
        future_df.sort_values(by=[1], inplace=True)
    future_df = future_df.loc[:, 3:]
    cursor.close()
    return future_df


def get_past_matchups():
    logging.info("Grabbing past UFC fights...")
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM past_matchups")
    fights_df = pd.DataFrame(cursor.fetchall()).loc[:, 1:]
    cursor.close()
    return fights_df
