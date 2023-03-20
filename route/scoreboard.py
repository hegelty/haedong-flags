from flask import Blueprint, render_template, request, redirect, make_response, jsonify
from tools import user_tools, db_tools

scoreboard_router = Blueprint('scoreboard', __name__, url_prefix='/scoreboard')

'''
@scoreboard_router.route('/', methods=['GET'])
def scoreboard_get():
    conn = db_tools.get_conn()
    curs = conn.cursor()
    curs.execute('select name, student_id, score, solved, solved_oobal from user order by score desc')
    data = curs.fetchall()
    for i in range(len(data)):
        data[i] = [
            data[i][0],
            data[i][1],
            data[i][2],
            data[i][3],
            list(map(lambda x: int(x) if x.isdigit() else 0, data[i][4].split(',')[1:]))
        ]
    curs.execute('select name, student_id, problem_id, problem_type, time from history order by time desc limit 20')
    history = curs.fetchall()
    return render_template('scoreboard/scoreboard.html', data=data, history=history)
'''


@scoreboard_router.route('/api', methods=['GET'])
def scoreboard_api():
    conn = db_tools.get_conn()
    curs = conn.cursor()
    curs.execute('select * from problem')
    problem_len = len(curs.fetchall())
    curs.execute('select * from problem_oobal')
    oobal_len = len(curs.fetchall())
    curs.execute('select name, student_id, score, solved, solved_oobal from user order by score desc')
    data = curs.fetchall()
    for i in range(len(data)):
        solved = []
        for j in range(data[i][3]):
            solved.append(True)
        for j in range(data[i][3], problem_len):
            solved.append(False)

        if user_tools.get_user_solved_oobal():
            for j in range(1,oobal_len+1):
                solved.append(str(j) in data[i][4].split(',')[1:])

        data[i] = {
            "name": data[i][0],
            "student_id": data[i][1],
            "score": data[i][2] if user_tools.get_user_solved_oobal() else min(data[i][2],101),
            "solved": solved
        }
    return {
        "success": True,
        "login": user_tools.login_check(),
        "oobal": user_tools.get_user_solved_oobal() == 1,
        "problem_len": problem_len,
        "oobal_len": oobal_len if user_tools.get_user_solved_oobal() else 0,
        "data": data
    }
