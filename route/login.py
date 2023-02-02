from flask import Blueprint, render_template, request, redirect, make_response
import requests
from tools import user_tools, db_tools

secret_key = open('oauth_key', 'r').read()
login_router = Blueprint('login', __name__, url_prefix='/login')


@login_router.route('/', methods=['GET'])
def login_get():
    return render_template('login/login.html')


@login_router.route('/callback', methods=['GET'])
def login_post():
    code = request.args.get('code')
    resp = requests.post('http://localhost:3000/oauth2/auth', params={
        'client_id': 'hd-flag',
        'scope': 'id'
    }, data={
        'client_secret': secret_key,
        'code': code
    })

    if resp.status_code != 200:
        return render_template('login/login.html', error='로그인에 실패했습니다.')

    token = resp.json()['access_token']

    resp = requests.post('http://localhost:3000/ex/user/info', data={
        'token': token,
        'client_id': 'hd-flag'
    })

    session_id, expire = user_tools.make_session(resp.json()['id'])

    conn = db_tools.get_conn()
    curs = conn.cursor()
    curs.execute('select id from user where id = ?', [resp.json()['id']])

    if not curs.fetchall():
        response = make_response(redirect('/login/register'))
        response.set_cookie(key='session_id', value=session_id, httponly=True, secure=True, expires=60 * 60 * 24 * 365,
                            max_age=60 * 60 * 24 * 365)
        return response

    response = make_response(redirect('/'))
    response.set_cookie(key='session_id', value=session_id, httponly=True, secure=True, expires=60 * 60 * 24 * 365,
                        max_age=60 * 60 * 24 * 365)
    return response


@login_router.route('/register', methods=['GET'])
@user_tools.require_login
def register_get():
    return render_template('login/register.html')


@login_router.route('/register', methods=['POST'])
@user_tools.require_login
def register_post():
    name = request.form.get('name')
    student_id = request.form.get('student_id')

    if len(name) > 6:
        return render_template('login/register.html', error='이름은 6글자를 넘을 수 없습니다.')

    if not student_id.isdigit() or len(student_id) != 4:
        return render_template('login/register.html', error='학번은 네자리 숫자로만 입력해주세요.')

    conn = db_tools.get_conn()
    curs = conn.cursor()

    session = request.cookies.get('session_id')
    user_id = user_tools.get_user_id(session)

    curs.execute('insert into user (id, name, student_id, score, solved, solved_oobal) values (?, ?, ?, ?, ?, ?)',
                 [user_id, name, int(student_id), 0, 0, ','])
    conn.commit()

    return redirect('/')
