from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

bp_admin = Blueprint('bp_admin', __name__)


@bp_admin.before_request
def before_request():
    if not current_user.admin:
        return redirect(url_for('bp_open.index'))


@bp_admin.get('/')
@login_required
def admin():
    return render_template('admin.html')
