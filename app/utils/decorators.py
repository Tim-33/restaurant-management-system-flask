from functools import wraps
from flask import request

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