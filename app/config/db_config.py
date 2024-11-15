from flask_mysqldb import MySQL
import MySQLdb
import logging

class DBConfig:
    def __init__(self, app):
        self.mysql = MySQL(app)
        self.app = app

    @property
    def connection(self):
        try:
            print("Connecting to database")
            connection = self.mysql.connection
            # Test the connection
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return connection
        except MySQLdb.OperationalError as e:
            logging.error(f"Database connection error: {e}")
            # Attempt to reconnect
            self.mysql = MySQL(self.app)
            return self.mysql.connection