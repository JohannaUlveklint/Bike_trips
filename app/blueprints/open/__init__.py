import datetime

from unidecode import unidecode
from geopy.geocoders import Nominatim
import requests

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

#
# def remove_non_ascii(text):
#     return unidecode(text)


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
    s_lat, s_long, e_lat, e_long = lat_long(start, end)
    route = get_route(s_lat, s_long, e_lat, e_long)
    return render_template('showroute.html', start=start, end=end, route=route)


# Am I thinking wrong here?
@bp_open.get('/showroute')
def show_route(start, end, route):
    start = start
    end = end
    route = route


def get_route(s_lat, s_long, e_lat, e_long):
    # api_key = "5b3ce3597851110001cf6248680f561c9c8640959dd1ecf9bf79f809"
    if not all([s_long, s_lat, e_long, e_lat]):  # Make an exception on this?
        print("Missing geo-coordinates")
        return None

    # search = f'api_key={api_key}&start={s_long},{s_lat}&end={e_long},{e_lat}'
    # response = requests.get('https://api.openrouteservice.org/v2/directions/cycling-regular?' + search)
    body = {"coordinates": [[s_long, s_lat], [e_long, e_lat]], "elevation": "true",
            "geometry": "true"}

    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': '5b3ce3597851110001cf6248680f561c9c8640959dd1ecf9bf79f809',
        'Content-Type': 'application/json; charset=utf-8'
    }
    response = requests.post('https://api.openrouteservice.org/v2/directions/cycling-regular', json=body,
                             headers=headers)
    if not response.ok:
        return 'Bad Request!'
    response = response.json()
    return response


# def distance_duration(s_lat, s_long, e_lat, e_long):
#     route = get_route(s_lat, s_long, e_lat, e_long)
#     distance = route['features'][0]['properties']['segments'][0]['distance']
#     duration = route['features'][0]['properties']['segments'][0]['duration']
#     return distance, duration


def lat_long(start, end):
    geolocator = Nominatim(user_agent="my_application", timeout=15)
    s = geolocator.geocode(start)
    e = geolocator.geocode(end)
    s_lat = str(s.latitude)
    s_long = str(s.longitude)
    e_lat = str(e.latitude)
    e_long = str(e.longitude)
    return s_lat, s_long, e_lat, e_long




def main():
    route = search_route_post()
    print(route)


if __name__ == '__main__':
    main()