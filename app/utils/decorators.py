from functools import wraps
from flask import request
import mysql.connector
from app import app

def log_request(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print(f"Request to {request.path} with data: {request.get_json()}")
            return f(*args, **kwargs)
        return decorated_function


def require_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return {"error": "Request must be JSON"}, 400
        return f(*args, **kwargs)
    return decorated_function

def with_db_connection(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        connection = mysql.connector.connect(
            host=app.config['MYSQL_DATABASE_HOST'],
            port=app.config['MYSQL_DATABASE_PORT'],
            user=app.config['MYSQL_DATABASE_USER'],
            password=app.config['MYSQL_DATABASE_PASSWORD'],
            database=app.config['MYSQL_DATABASE_DB']
        )
        self.cursor = connection.cursor()
        try:
            result = func(self, *args, **kwargs)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            self.cursor.close()
            connection.close()
        return result
    return wrapper