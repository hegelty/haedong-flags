import datetime
import random
import string
from tools import db_tools
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
            return {
                'success': False,
                'code': -1
            }
        if sessions[session_id]["expire"] < datetime.datetime.now():
            del (sessions[session_id])
            return {
                'success': False,
                'code': -2
            }

        renew_session(session_id)

        return func(*args, **kwargs)
    decorator.__name__ = func.__name__
    return decorator


def get_user_id():
    session = request.cookies.get('session_id')
    return sessions[session]["user_id"]


def login_check():
    session = request.cookies.get('session_id')
    if session not in sessions:
        return False
    if sessions[session]["expire"] < datetime.datetime.now():
        del (sessions[session])
        return False
    renew_session(session)
    return True


def get_user_info():
    session = request.cookies.get('session_id')
    conn = db_tools.get_conn()
    curs = conn.cursor()
    curs.execute('select name, student_id, solved, solved_oobal, score from user where id = ?', [sessions[session]["user_id"]])
    data = curs.fetchone()
    return {
        'success': True,
        'id': sessions[session]["user_id"],
        'name': data[0],
        'student_id': data[1],
        'solved': int(data[2]),
        'solved_oobal': data[3].split(','),
        'oobal': get_user_solved_oobal(),
        'score': data[4]
    }


def get_user_info_2():
    session = request.cookies.get('session_id')
    conn = db_tools.get_conn()
    curs = conn.cursor()
    curs.execute('select * from problem')
    problem_len = len(curs.fetchall())
    curs.execute('select * from problem_oobal')
    oobal_len = len(curs.fetchall())

    curs.execute('select name, student_id, solved, solved_oobal, score from user where id = ?', [sessions[session]["user_id"]])
    data = curs.fetchone()

    solved = []
    for i in range(data[2]):
        solved.append(True)
    for i in range(problem_len - data[2]):
        solved.append(False)

    if get_user_solved_oobal():
        for i in range(1, oobal_len + 1):
            solved.append(str(i) in data[3].split(',')[1:])

    return {
        'success': True,
        'id': sessions[session]["user_id"],
        'name': data[0],
        'student_id': data[1],
        'solved': solved,
        "problem_len": problem_len,
        "oobal_len": oobal_len if get_user_solved_oobal() else 0,
        'oobal': get_user_solved_oobal() == 1,
        'score': data[4]
    }


def get_user_solved_oobal():
    try:
        session = request.cookies.get('session_id')
        conn = db_tools.get_conn()
        curs = conn.cursor()
        curs.execute('select solved_oobal from user where id = ?', [sessions[session]["user_id"]])
        data = [i for i in curs.fetchone() if i!='']
        return 1 if len(data) > 0 else 0
    except:
        return 0


def add_solved(problem_id):
    session = request.cookies.get('session_id')
    conn = db_tools.get_conn()
    curs = conn.cursor()
    user = get_user_info()
    curs.execute('update user set solved = solved + 1 where id = ?', [sessions[session]["user_id"]])
    curs.execute('select score from problem where id = ?', [problem_id])
    curs.execute('update user set score = score + ? where id = ?', [curs.fetchone()[0], sessions[session]["user_id"]])
    curs.execute('insert into history (id, name, student_id, problem_id, problem_type, time) values (?, ?, ?, ?, ?, ?)',
                 [sessions[session]["user_id"], user['name'], user['student_id'] , problem_id, '', datetime.datetime.now()])
    conn.commit()


def add_solved_oobal(problem_id):
    session = request.cookies.get('session_id')
    conn = db_tools.get_conn()
    curs = conn.cursor()
    user = get_user_info()
    solved_oobal = user['solved_oobal']
    solved_oobal.append(str(problem_id))

    curs.execute('update user set solved_oobal = ? where id = ?', [','.join(solved_oobal), sessions[session]["user_id"]])
    curs.execute('select score from problem_oobal where id = ?', [problem_id])
    curs.execute('update user set score = score + ? where id = ?', [curs.fetchone()[0], sessions[session]["user_id"]])
    curs.execute('insert into history (id, name, student_id, problem_id, problem_type, time) values (?, ?, ?, ?, ?, ?)',
                 [sessions[session]["user_id"], user['name'], user['student_id'] , problem_id, '우발', datetime.datetime.now()])
    conn.commit()
