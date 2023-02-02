from flask import Blueprint, render_template, request, redirect, flash, Response
from tools import user_tools, db_tools

oobal_router = Blueprint('oobal', __name__, url_prefix='/oobal')



@oobal_router.route('/', methods=['GET'])
@user_tools.require_login
def submit_oobal_home():
    user_info = user_tools.get_user_info()
    return render_template('submit/submit_oobal_home.html', solved_oobal=user_info['solved_oobal'])


@oobal_router.route('/<int:id>', methods=['GET'])
@user_tools.require_login
def submit_oobal_get(id):
    if str(id) in user_tools.get_user_info()['solved_oobal']:
        return redirect('/oobal')
    return render_template('submit/submit_oobal.html', id=id)


@oobal_router.route('/<int:id>', methods=['POST'])
@user_tools.require_login
def submit_oobal_post(id):
    if str(id) in user_tools.get_user_info()['solved_oobal']:
        return Response(status=403)

    conn = db_tools.get_conn()
    curs = conn.cursor()
    curs.execute('select answer from problem_oobal where id = ?', [id])

    if request.form['flag'] == curs.fetchone()[0]:
        user_tools.add_solved_oobal(id)
        return {
            'success': True
        }

    return {
        'success': False,
        'error': '플래그가 틀렸습니다.'
    }
