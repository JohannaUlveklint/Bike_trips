from flask import Blueprint, render_template

bp_user = Blueprint('bp_user', __name__)


@bp_user.get('/')
def user_index():
    return "User Profile Page"
