from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User
from flask import current_app as app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Account created. Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid credentials.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# --- Новые маршруты редактирования ---
@app.route('/edit-name', methods=['GET', 'POST'])
@login_required
def edit_name():
    if request.method == 'POST':
        current_user.name = request.form['name']
        db.session.commit()
        flash('Name updated.')
        return redirect(url_for('home'))
    return render_template('edit_name.html', user=current_user)

@app.route('/edit-email', methods=['GET', 'POST'])
@login_required
def edit_email():
    if request.method == 'POST':
        current_user.email = request.form['email']
        db.session.commit()
        flash('Email updated.')
        return redirect(url_for('home'))
    return render_template('edit_email.html', user=current_user)

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        if current_user.check_password(current_password):
            current_user.set_password(new_password)
            db.session.commit()
            flash('Password changed.')
            return redirect(url_for('home'))
        else:
            flash('Current password is incorrect.')
    return render_template('change_password.html')
