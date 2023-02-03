from flask import Blueprint, render_template, request, redirect, make_response, jsonify
from tools import user_tools, db_tools

scoreboard_router = Blueprint('scoreboard', __name__, url_prefix='/scoreboard')


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


@scoreboard_router.route('/api', methods=['GET'])
def scoreboard_api():
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
        ] if user_tools.login_check() else [
            data[i][0],
            data[i][1],
            data[i][2],
            data[i][3]
        ]
    return jsonify(data)
