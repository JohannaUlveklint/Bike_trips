# import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager

from app.persistance.db import init_db


def create_app():
    _app = Flask(__name__)
    _app.config['SECRET_KEY'] = 'ed7d2a5786f44a7e646ce1d538647a4339e9be587384632eafad8b763661ec7f'  # Change and put
    # in .env?

    login_manager = LoginManager()
    login_manager.init_app(_app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.persistance.models import User
        return User.find(email=user_id).first_or_none()

    from app.blueprints.open import bp_open
    _app.register_blueprint(bp_open)

    from app.blueprints.user import bp_user
    _app.register_blueprint(bp_user, url_prefix='/user')

    from app.blueprints.admin import bp_admin
    _app.register_blueprint(bp_admin, url_prefix='/admin')

    @_app.context_processor
    def utility_processor():
        def hhmmss(duration):
            base_date = datetime(1, 1, 1, 0, 0, 0, 0)
            t = base_date + timedelta(seconds=duration)
            time = t.strftime('%H:%M:%S')
            return time

        return dict(hhmmss=hhmmss)

    @_app.context_processor
    def utility_processor():
        def date_without_ms(date):
            without = date.strftime("%Y-%m-%d %H:%M:%S")
            return without

        return dict(date_time=date_without_ms)

    @_app.context_processor
    def utility_processor():
        def distance_rounded(distance):
            rounded = round((distance / 1000), 3)
            return rounded

        return dict(rounded_distance=distance_rounded)

    return _app


if __name__ == '__main__':
    load_dotenv()
    app = create_app()
    app.run()
