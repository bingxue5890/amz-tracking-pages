from flask import Flask, request, jsonify, render_template, send_from_directory, session, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import logging

app = Flask(__name__)

# 确保instance目录存在
if not os.path.exists('instance'):
    os.makedirs('instance')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///instance/users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化扩展
db = SQLAlchemy(app)
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 用户模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# 路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    
    if user and user.check_password(data.get('password')):
        login_user(user)
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': '用户名或密码错误'})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first():
        return jsonify({'success': False, 'error': '用户名已存在'})
    
    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'error': '邮箱已被注册'})
    
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')

@app.route('/fetch_tracking', methods=['POST'])
def fetch_tracking():
    try:
        data = request.get_json()
        tba_number = data.get('tba_number')
        
        if not tba_number:
            logger.warning('No TBA number provided')
            return jsonify({'success': False, 'error': '请输入TBA单号'})

        # 检查track目录是否存在
        if not os.path.exists('track'):
            os.makedirs('track')
            logger.info('Created track directory')

        # 检查track目录是否存在对应的HTML文件
        track_file = os.path.join('track', f'{tba_number}.html')
        if os.path.exists(track_file):
            logger.info(f'Found tracking file for {tba_number}')
            return jsonify({
                'success': True,
                'url': f'/track/{tba_number}.html'
            })
        
        logger.warning(f'No tracking file found for {tba_number}')
        return jsonify({
            'success': False,
            'error': '未找到该单号的轨迹信息'
        })

    except Exception as e:
        logger.error(f'Error in fetch_tracking: {str(e)}')
        return jsonify({
            'success': False,
            'error': '服务器内部错误，请稍后重试'
        })

@app.route('/track/<path:filename>')
def serve_track_file(filename):
    try:
        return send_from_directory('track', filename)
    except Exception as e:
        logger.error(f'Error serving track file {filename}: {str(e)}')
        return jsonify({
            'success': False,
            'error': '文件访问错误'
        })

# WebSocket事件处理
connected_users = set()

@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        connected_users.add(current_user.id)
        emit('online_users', len(connected_users), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    if current_user.is_authenticated:
        connected_users.remove(current_user.id)
        emit('online_users', len(connected_users), broadcast=True)

@socketio.on('message')
def handle_message(data):
    if current_user.is_authenticated:
        data['username'] = current_user.username
        emit('message', data, broadcast=True)

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'success': False, 'error': '页面未找到'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, host='0.0.0.0', port=8080, debug=True) 