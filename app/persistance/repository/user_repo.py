from app.persistance.models import User


def get_all_users():
    return User.all()
