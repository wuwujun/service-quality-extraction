import pymysql
from DBUtils.PooledDB import PooledDB
import settings.db_config as config


class ConnectionPool(object):

    def __init__(self):
        self.pool = None

    def __enter__(self):
        self.conn = self.get_conn()
        self.cursor = self.conn.cursor()
        return self

    def get_conn(self):
        if self.pool is None:
            self.pool = PooledDB(creator=pymysql,
                                 mincached=config.DB_MIN_CACHED,
                                 maxcached=config.DB_MAX_CACHED,
                                 maxconnections=config.DB_MAX_CONNECTIONS,
                                 maxshared=config.DB_MAX_SHARED,
                                 blocking=config.DB_BLOCKING,
                                 maxusage=config.DB_MAX_USAGE,
                                 setsession=config.DB_SET_SESSION,
                                 host=config.DB_HOST,
                                 user=config.DB_USER,
                                 passwd=config.DB_PASSWORD,
                                 db=config.DB_NAME,
                                 charset=config.DB_CHARSET)
            return self.pool.connection()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

