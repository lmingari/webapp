from app.profiles.routes import bp
from flask import redirect, url_for, flash, session
from functools import wraps

def profile_required(func):
    @wraps(func)
    def inner1(*args, **kwargs):
        if session.get('profile') is None:
            flash("A profile must be loaded")
            return redirect(url_for('profiles.index'))
        return func(*args, **kwargs)
    return inner1
