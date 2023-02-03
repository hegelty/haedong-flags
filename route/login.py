from flask import Blueprint, render_template, request, redirect, make_response, Response
import requests
from tools import user_tools, db_tools, oauth

secret_key = open('oauth_key', 'r').read()
login_router = Blueprint('login', __name__, url_prefix='/login')


@login_router.route('/', methods=['GET'])
def login_post():
    code = request.args.get('code')
    resp = requests.post(oauth.domain+'/oauth2/auth', params={
        'client_id': oauth.id,
        'scope': 'id'
    }, data={
        'client_secret': secret_key,
        'code': code
    })

    if resp.status_code != 200:
        return Response(status=403)

    token = resp.json()['access_token']

    resp = requests.post(oauth.domain+'/ex/user/info', data={
        'token': token,
        'client_id': oauth.id
    })
    print(resp.text)
    conn = db_tools.get_conn()
    curs = conn.cursor()
    curs.execute('select id from user where id = ?', [resp.json()['id']])

    if not curs.fetchall():
        return {
            'success': False,
            'error':'등록되지 않은 유저입니다.',
            'session': user_tools.make_session(resp.json()['id'])[0]
        }

    session_id, expire = user_tools.make_session(resp.json()['id'])
    return {
            'success': True,
            'session_id': session_id
    }


@login_router.route('/register', methods=['POST'])
@user_tools.require_login
def register_post():
    name = request.form.get('name')
    student_id = request.form.get('student_id')

    if len(name) > 6:
        return {
            'success': False,
            'error':'이름은 6글자를 넘을 수 없습니다.'
        }

    if not student_id.isdigit() or len(student_id) != 4:
        return {
            'success': False,
            'error':'학번은 네자리 숫자로만 입력해주세요.'
        }

    user_id = user_tools.get_user_id(request.cookies.get('session_id'))
    conn = db_tools.get_conn()
    curs = conn.cursor()
    curs.execute('select id from user where id = ?', [user_id])

    if curs.fetchall():
        return {
            'success': False,
            'errer':'이미 등록된 계정입니다.'
        }

    curs.execute('insert into user (id, name, student_id, score, solved, solved_oobal) values (?, ?, ?, ?, ?, ?)',
                 [user_id, name, int(student_id), 0, 0, ''])
    conn.commit()

    return {
            'success': True
    }
