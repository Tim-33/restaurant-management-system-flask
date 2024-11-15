from functools import wraps
from flask import request, Flask

def log_request(app: Flask):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            app.logger.info(f"Request to {request.path} with data: {request.get_json()}")
            return f(*args, **kwargs)
        return decorated_function
    return decorator