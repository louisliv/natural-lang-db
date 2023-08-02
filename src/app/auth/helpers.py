from functools import wraps

from flask import flash, redirect, url_for, request

from app.auth.token_authentication import TokenAuthentication


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        is_authenticated = TokenAuthentication(request).is_authenticated()
        if is_authenticated:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for("login"))

    return wrap
