import datetime
import random
import string

from flask import request, redirect

sessions = {}


def make_session(user_id):
    session_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(64))
    sessions[session_id] = {
        "user_id": user_id,
        "expire": datetime.datetime.now() + datetime.timedelta(minutes=60)
    }
    return session_id, sessions[session_id]["expire"]


def renew_session(session_id):
    if sessions[session_id]["expire"] < datetime.datetime.now():
        return False
    sessions[session_id]["expire"] = datetime.datetime.now() + datetime.timedelta(minutes=60)
    return True


def require_login(func):
    def decorator(*args, **kwargs):
        session_id = request.cookies.get('session_id')
        if session_id not in sessions:
            return redirect('/login')
        if sessions[session_id]["expire"] < datetime.datetime.now():
            del (sessions[session_id])
            return redirect('/login')

        renew_session(session_id)

        return func()

    return decorator
