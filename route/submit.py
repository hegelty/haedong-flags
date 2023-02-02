from flask import Blueprint, render_template, request, redirect
from tools import user_tools, db_tools

submit_router = Blueprint('submit', __name__, url_prefix='/submit')


@submit_router.route('/', methods=['GET'])
@user_tools.require_login
def submit_home():
    user_info = user_tools.get_user_info()
    return render_template('submit/submit_home.html', solved=user_info['solved'], solved_oobal=user_info['solved_oobal'])


@submit_router.route('/<int:problem_id>', methods=['GET'])
@user_tools.require_login
def submit_get(problem_id):
    if user_tools.get_user_info()['solved'] + 1 != problem_id:
        return redirect('/submit')

    return render_template('submit/submit.html', id=problem_id)


@submit_router.route('/<int:problem_id>', methods=['POST'])
@user_tools.require_login
def submit_post(problem_id):
    if user_tools.get_user_info()['solved'] + 1 != problem_id:
        return redirect('/submit')

    conn = db_tools.get_conn()
    curs = conn.cursor()
    curs.execute('select answer from problem where id = ?', [problem_id])

    if request.form['flag'] == curs.fetchone()[0]:
        user_tools.add_solved(problem_id)
        return redirect('/submit')

    return render_template('submit/submit.html', id=problem_id, error='틀렸습니다.')
