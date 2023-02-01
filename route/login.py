from flask import Blueprint, render_template, request, redirect, make_response
import requests
from tools import login_tools

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

    session_id, expire = login_tools.make_session(resp.json()['id'])
    print(session_id)
    response = make_response(redirect('/'))
    response.set_cookie(key='session_id', value=session_id, httponly=True, secure=True, expires=60 * 60, max_age=3600)
    return response
