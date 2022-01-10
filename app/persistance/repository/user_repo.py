from app.persistance.models import User


def get_all_users():
    return User.all()


def user_trips(email):
    user = User.find(email=email).first_or_none()
    print()
    trips = [trip for trip in user.trips]
    return trips
