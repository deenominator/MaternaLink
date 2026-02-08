from flask import session, abort
from functools import wraps

def login_is_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        return f(*args, **kwargs)
    return wrapper
