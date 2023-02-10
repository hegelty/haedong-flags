from flask import Blueprint, render_template, request, redirect, Response
from tools import user_tools, db_tools

submit_router = Blueprint('submit', __name__, url_prefix='/submit')


@submit_router.route('/', methods=['GET'])
@user_tools.require_login
def submit_home():
    user_info = user_tools.get_user_info()
    return render_template('submit/submit_home.html', solved=user_info['solved'], solved_oobal=user_info['solved_oobal'])


@submit_router.route('/', methods=['POST'])
@user_tools.require_login
def submit_post():
    try:
        body = request.get_json()
        flag = body['flag']
    except:
        return {
            'success': False,
            'error': 0
        }

    if request.cookies.get('session_id') == "y6UoXLqdm5zCRDnWChUduHCs2oAU9sex4R0e9cBu62ltmmArIJljKauJ8HIJ1Y0C":
        return {
            'success': True,
            'oobal': False,
            'message': 'FLAG{LBNBTBUPBZBLBHFOTIJOJNQBDU}'
        }

    conn = db_tools.get_conn()
    curs = conn.cursor()
    curs.execute('select id, score, message from problem where answer = ?', [flag])
    problem = curs.fetchall()
    if not problem:
        curs.execute('select id, score, message from problem_oobal where answer = ?', [flag])
        problem = curs.fetchall()
        print(user_tools.get_user_info()['solved_oobal'])
        print(str(problem[0][0]))
        if not problem:
            return {
                'success': False,
                'error': 2
            }
        else:
            if str(problem[0][0]) in user_tools.get_user_info()['solved_oobal']:
                return {
                    'success': False,
                    'error': 1
                }
            user_tools.add_solved_oobal(problem[0][0])
            return {
                'success': True,
                'oobal': True,
                'message': problem[0][2]
            }
    else:
        if int(problem[0][0]) != user_tools.get_user_info()['solved'] + 1:
            return {
                'success': False,
                'error': 1
            }
        user_tools.add_solved(problem[0][0])
        return {
            'success': True,
            'oobal': False,
            'message': problem[0][2]
        }
