
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super-idv-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///idv.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/content')
    return redirect('/login')

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_api():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['user_id'] = user.id
        return jsonify(success=True)
    return jsonify(success=False, message='账号或密码错误')

@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_api():
  # 前端post用application/json
    if request.is_json:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
    else:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
    if len(username) < 4 or len(password) < 6:
        return jsonify(error='用户名/密码太短')
    if User.query.filter_by(username=username).first():
        return jsonify(error='用户名已被注册')
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(message='注册成功')

@app.route('/content')
def content():
    if 'user_id' not in session:
        return redirect('/login')
    # 简易角色数据，可以自行扩充
    roles = {
        "jgz": [
            {"name": "杰克", "img": "https://id5.res.netease.com/pc/gw/20220408094220/img/role/jack.png", "desc": "监管者，绅士杀手，拥有雾刃技能。"},
            {"name": "厂长", "img": "https://id5.res.netease.com/pc/gw/20220408094220/img/role/bane.png", "desc": "监管者，能召唤傀儡，控制全场。"}
        ],
        "qsz": [
            {"name": "医生", "img": "https://id5.res.netease.com/pc/gw/20220408094220/img/role/doctor.png", "desc": "求生者，擅长治疗自己和队友。"},
            {"name": "律师", "img": "https://id5.res.netease.com/pc/gw/20220408094220/img/role/lawyer.png", "desc": "求生者，能查看地图，辅助全队。"}
        ]
    }
    return render_template('content.html', roles=roles)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
