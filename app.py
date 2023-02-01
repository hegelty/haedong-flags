from flask import Flask, render_template
from route import login
from tools import login_tools

app = Flask(__name__)
app.register_blueprint(login.login_router)


@app.route('/')
@login_tools.require_login
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
