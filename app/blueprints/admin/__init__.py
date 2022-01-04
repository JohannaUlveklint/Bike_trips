from flask import Blueprint, render_template

bp_admin = Blueprint('bp_admin', __name__)


@bp_admin.get('/')
def admin_index():
    return "Admin index page"

