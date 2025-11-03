from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User, ServiceRequest
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'medical_app.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'change_this_to_a_secret_key'

# initialize DB
db.init_app(app)

with app.app_context():
    db.create_all()
    # Create a default admin if not exists
    admin_email = 'admin@example.com'
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(name='Admin', email=admin_email, password_hash=generate_password_hash('adminpass'), is_admin=True)
        db.session.add(admin)
        db.session.commit()

# --------- Helpers ---------

def current_user():
    uid = session.get('user_id')
    if not uid:
        return None
    return User.query.get(uid)

# --------- Routes: Auth ---------

@app.route('/')
def index():
    user = current_user()
    if user:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email') or None
        phone = request.form.get('phone') or None
        password = request.form.get('password')
        if not password or (not email and not phone):
            flash('Provide email or phone and a password')
            return redirect(url_for('register'))
        # uniqueness check
        if email:
            if User.query.filter_by(email=email).first():
                flash('Email already registered')
                return redirect(url_for('register'))
        if phone:
            if User.query.filter_by(phone=phone).first():
                flash('Phone already registered')
                return redirect(url_for('register'))
        user = User(name=name, email=email, phone=phone, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier')
        password = request.form.get('password')
        # identifier can be email or phone
        user = None
        if '@' in (identifier or ''):
            user = User.query.filter_by(email=identifier).first()
        else:
            user = User.query.filter_by(phone=identifier).first()
        if user and check_password_hash(user.password_hash, password):
            session.clear()
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            flash('Logged in successfully')
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out')
    return redirect(url_for('login'))

# --------- User Dashboard & Booking ---------

@app.route('/dashboard')
def dashboard():
    user = current_user()
    if not user:
        return redirect(url_for('login'))
    requests = ServiceRequest.query.filter_by(user_id=user.id).order_by(ServiceRequest.created_at.desc()).all()
    return render_template('dashboard.html', user=user, requests=requests)

@app.route('/book', methods=['GET','POST'])
def book_service():
    user = current_user()
    if not user:
        return redirect(url_for('login'))
    if request.method == 'POST':
        service_type = request.form.get('service_type')
        details = request.form.get('details')
        sr = ServiceRequest(user_id=user.id, service_type=service_type, details=details, status='Pending')
        db.session.add(sr)
        db.session.commit()
        flash('Service requested successfully')
        return redirect(url_for('dashboard'))
    return render_template('book_service.html')

@app.route('/track')
def track_status():
    user = current_user()
    if not user:
        return redirect(url_for('login'))
    requests = ServiceRequest.query.filter_by(user_id=user.id).order_by(ServiceRequest.created_at.desc()).all()
    return render_template('track_status.html', requests=requests)

# --------- Admin ---------

@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, is_admin=True).first()
        if user and check_password_hash(user.password_hash, password):
            session.clear()
            session['user_id'] = user.id
            session['is_admin'] = True
            flash('Admin logged in')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid admin credentials')
        return redirect(url_for('admin_login'))
    return render_template('admin_login.html')

@app.route('/admin')
def admin_dashboard():
    uid = session.get('user_id')
    if not uid or not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    requests = ServiceRequest.query.order_by(ServiceRequest.created_at.desc()).all()
    return render_template('admin_dashboard.html', requests=requests)

@app.route('/admin/update', methods=['POST'])
def admin_update():
    uid = session.get('user_id')
    if not uid or not session.get('is_admin'):
        flash('Not authorized')
        return redirect(url_for('admin_login'))
    action = request.form.get('action')
    rid = request.form.get('request_id')
    sr = ServiceRequest.query.get(rid)
    if not sr:
        flash('Request not found')
        return redirect(url_for('admin_dashboard'))
    if action == 'accept':
        sr.status = 'Accepted'
    elif action == 'complete':
        sr.status = 'Completed'
    db.session.commit()
    flash('Status updated')
    return redirect(url_for('admin_dashboard'))

# --------- Run ---------

if __name__ == '__main__':
    app.run(debug=True)