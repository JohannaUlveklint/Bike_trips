import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash

from app.controller.user_controller import create_user

bp_open = Blueprint('bp_open', __name__)


@bp_open.get('/')
def index():
    return render_template('index.html')


@bp_open.get('/signin')
def signin_get():
    return render_template('signin.html')


@bp_open.post('/signin')
def signin_post():
    email = request.form.get('email')
    password = request.form.get('password')
    from app.persistance.models import User
    user = User.find(email=email).first_or_none()
    if user is None:
        flash('Error signing in. Check your email and password!')
        return redirect(url_for('bp_open.signin_get'))

    if not check_password_hash(user.password, password):
        flash('Error signing in. Check your email and password!')
        return redirect(url_for('bp_open.signin_get'))

    login_user(user)
    user.last_signin = datetime.datetime.now()
    user.save()
    return redirect(url_for('bp_user.user'))  # Should I also return user email?


@bp_open.get('/signup')
def signup_get():
    return render_template('signup.html')


@bp_open.post('/signup')
def signup_post():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')

    from app.persistance.models import User
    user = User.find(email=email).first_or_none()
    # Check if a user with this email exists in the db
    # If so, give error message, stay on the sign-up page
    if user is not None:
        flash('Email address already exists!')
        return redirect(url_for('bp_open.signup_get'))

    # If not, create a user with the password hashed, and save it to the db
    # Redirect to the sign in page
    create_user(first_name, last_name, email, password)
    return redirect(url_for('bp_open.signin_get'))


@bp_open.get('/signout')  # Should this be in user?
@login_required
def signout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('bp_open.index'))


@bp_open.get('/searchroute')
def search_route():
    return render_template('searchroute.html')


@bp_open.post('/searchroute')
def search_route_post():
    start = request.form.get('start')
    end = request.form.get('end')