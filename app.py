from flask import Flask, render_template, jsonify
from flask_cors import CORS
from route import login, submit, submit_oobal, scoreboard
from tools import user_tools, db_tools, oauth

app = Flask(__name__)
CORS(app, supports_credentials=True,
     resources={
         r"*": {
             "origin": "*"
         },
     })
app.register_blueprint(login.login_router)
app.register_blueprint(submit.submit_router)
app.register_blueprint(submit_oobal.oobal_router)
app.register_blueprint(scoreboard.scoreboard_router)


@app.route('/')
@user_tools.require_login
def index():
    return render_template('index.html')


@app.route('/user/info')
@user_tools.require_login
def user_info():
    return jsonify(user_tools.get_user_info())


if __name__ == '__main__':
    db_tools.db_init()
    app.run(host='0.0.0.0', port=8000)
