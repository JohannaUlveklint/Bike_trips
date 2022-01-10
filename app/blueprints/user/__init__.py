from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.controller.user_controller import user_trips

bp_user = Blueprint('bp_user', __name__)


# @bp_user.get('/')
# def user_index():
#     return "User Profile Page"

@bp_user.get('/')
@login_required
def user():
    return render_template('user.html')


@bp_user.get('/savedtrips')
@login_required
def saved_trips():
    from app.persistance.models import User
    # trips = current_user.trips
    # if trips is None:
    #     return '<h3> You have no saved trips </h3>'
    # else:
    return render_template('savedtrips.html')
    # user_trips = User.find({"trips":{$ne:null}}).first_or_none()

    # from app.persistance.models import User
    # user = User.find(email=email).first_or_none()
    # if user is None:
    #     flash('Error signing in. Check your email and password!')
    #     return redirect(url_for('bp_open.signin_get'))
    #
    # if not check_password_hash(user.password, password):
    #     flash('Error signing in. Check your email and password!')
    #     return redirect(url_for('bp_open.signin_get'))

