from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'telecom-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///telecom.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# DATABASE MODELS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    avatar = db.Column(db.String(10), default='U')
    created_at = db.Column(db.DateTime, default=datetime.now)

class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    plan_name = db.Column(db.String(50), default='Standard')
    plan_price = db.Column(db.Float, default=599)
    calls = db.Column(db.Integer, default=1500)
    sms = db.Column(db.Integer, default=300)
    data = db.Column(db.Float, default=15)

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Float, default=706.82)
    period = db.Column(db.String(20), default='February 2024')
    status = db.Column(db.String(20), default='pending')
    due_date = db.Column(db.DateTime, default=lambda: datetime.now() + timedelta(days=5))

class CallLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    number = db.Column(db.String(20))
    call_type = db.Column(db.String(20))
    duration = db.Column(db.Integer)
    cost = db.Column(db.Float, default=0)
    date_time = db.Column(db.DateTime, default=datetime.now)
    name = db.Column(db.String(50))

# ROUTES
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password, data['password']):
            session['user_id'] = user.id
            session['username'] = user.username
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'success': False, 'message': 'Username exists'}), 400
        user = User(username=data['username'], email=data['email'], full_name=data['full_name'], avatar=data['username'][0].upper())
        user.password = generate_password_hash(data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'success': True})
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/plans')
def plans_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('plans.html', user=user)

@app.route('/bills')
def bills_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('bills.html', user=user)

@app.route('/calls')
def calls_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('calls.html', user=user)

# API ENDPOINTS
@app.route('/api/user')
def get_user():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    user = User.query.get(session['user_id'])
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email, 'full_name': user.full_name, 'phone': user.phone, 'avatar': user.avatar})

@app.route('/api/plan')
def get_plan():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    plan = Plan.query.filter_by(user_id=session['user_id']).first()
    if plan:
        return jsonify({'name': plan.plan_name, 'price': plan.plan_price, 'calls': plan.calls, 'sms': plan.sms, 'data': plan.data})
    return jsonify({'name': 'Standard Plan', 'price': 599, 'calls': 1500, 'sms': 300, 'data': 15})

@app.route('/api/bill')
def get_bill():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    bill = Bill.query.filter_by(user_id=session['user_id']).first()
    if bill:
        return jsonify({'amount': bill.amount, 'period': bill.period, 'status': bill.status, 'due_date': bill.due_date.isoformat()})
    return jsonify({'amount': 706.82, 'period': 'February 2024', 'status': 'pending', 'due_date': (datetime.now() + timedelta(days=5)).isoformat()})

@app.route('/api/usage')
def get_usage():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify({'calls_used': 750, 'calls_limit': 1500, 'sms_used': 150, 'sms_limit': 300, 'data_used': 7.5, 'data_limit': 15})

@app.route('/api/calls')
def get_calls():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    calls = CallLog.query.filter_by(user_id=session['user_id']).order_by(CallLog.date_time.desc()).all()
    return jsonify([{'number': c.number, 'type': c.call_type, 'duration': c.duration, 'cost': c.cost, 'name': c.name, 'date': c.date_time.isoformat()} for c in calls])

@app.route('/api/bill/pay', methods=['POST'])
def pay_bill():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    bill = Bill.query.filter_by(user_id=session['user_id']).first()
    if bill:
        bill.status = 'paid'
        db.session.commit()
    return jsonify({'success': True, 'transaction_id': f'TXN{datetime.now().strftime("%Y%m%d%H%M%S")}'})

@app.route('/api/profile/update', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    user = User.query.get(session['user_id'])
    user.full_name = data.get('full_name', user.full_name)
    user.phone = data.get('phone', user.phone)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify({'success': True})

def init_db():
    with app.app_context():
        db.create_all()
        if User.query.count() == 0:
            user = User(username='testuser', email='test@telecom.com', full_name='Rajesh Kumar', phone='+91 9876543210', avatar='R')
            user.password = generate_password_hash('password123')
            db.session.add(user)
            db.session.commit()
            plan = Plan(user_id=user.id, plan_name='Standard Plan', plan_price=599, calls=1500, sms=300, data=15)
            bill = Bill(user_id=user.id, amount=706.82, period='February 2024', status='pending')
            call1 = CallLog(user_id=user.id, number='+91 9876543210', call_type='incoming', duration=435, cost=0, name='Mom')
            call2 = CallLog(user_id=user.id, number='+91 9123456789', call_type='outgoing', duration=240, cost=5, name='Friend')
            call3 = CallLog(user_id=user.id, number='+91 9999999999', call_type='incoming', duration=180, cost=0, name='Office')
            db.session.add_all([plan, bill, call1, call2, call3])
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)