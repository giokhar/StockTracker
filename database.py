import pymysql
import os


class Database:
    def __init__(self):
        self.con = pymysql.connect(
            os.getenv("DB_HOST"),
            os.getenv("DB_USER"),
            os.getenv("DB_PASS"),
            os.getenv("DB_NAME"),
            cursorclass=pymysql.cursors.DictCursor)

        self.cur = self.con.cursor()

    def get_log_for_portfolio(self, portfolio_id):
        return self.call_proc("GetLogForPortfolio", (portfolio_id,))

    def call_proc(self, proc, var_list=(), many=True):
        # if connection is lost, reconnect
        self.con.ping(reconnect=True)

        self.cur.callproc(proc, tuple(var_list))
        if many:
            result = self.cur.fetchall()
        else:
            result = self.cur.fetchone()
        return result
