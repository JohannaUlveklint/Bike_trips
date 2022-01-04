from flask import Blueprint, render_template

bp_open = Blueprint('bp_open', __name__)


@bp_open.get('/')
def index():
    # from app.controller.user_controller import get_all_users
    # users = get_all_users()
    return render_template('index.html')


@bp_open.get('/about')
def about():
    return render_template('about.html')


@bp_open.get('/cyclists')
def cyclists():
    from app.controller.user_controller import get_all_users
    users = get_all_users()
    return render_template('cyclists.html', users=users)


@bp_open.get('/trips')
def trips():
    from app.controller.trip_controller import get_all_trips
    all_trips = get_all_trips()
    return render_template('trips.html', trips=all_trips)  # trips returns to the jinja2 template, all_trips is the local variable

