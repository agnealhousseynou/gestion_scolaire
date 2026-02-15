from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from werkzeug.security import generate_password_hash

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Identifiant ou mot de passe incorrect.')
            
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/register_admin_initial', methods=['GET'])
def register_admin():
    # Route temporaire pour créer le premier admin
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', nom='Admin', prenom='System', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        return "Admin créé avec succès (admin / admin123)"
    return "Admin existe déjà"
