import mysql.connector


class MySqlDatabaseConnection:
    def __init__(self, host, user, password, database):
        self.con = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
        )
        self.create_past_matchups_table()
        self.create_future_matchups_table()

    def create_past_matchups_table(self):
        cursor = self.con.cursor()
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

        print(cursor.fetchone()[0])
        cursor.close()

    def create_future_matchups_table(self):
        cursor = self.con.cursor()
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
