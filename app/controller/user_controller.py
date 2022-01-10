import datetime

from flask import app
from werkzeug.security import generate_password_hash


from app.persistance.repository import user_repo


def create_user(first_name, last_name, email, password):
    from app.persistance.models import User
    user = User(
        {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': generate_password_hash(password),
            'admin': False,
            'date_created': datetime.datetime.now(),
            'last_signin': None,
            'activated': False
        }
    )
    user.save()


def user_trips(email):
    trips_db = user_repo.user_trips(email)
    base_date = datetime.datetime(1, 1, 1, 0, 0, 0, 0)
    # [setattr(trip, 'time', base_date + datetime.timedelta(seconds=trip.duration)) for trip in trips_db]
    trips = []
    for trip in trips_db:
        t = base_date + datetime.timedelta(seconds=trip['duration'])
        trip['time'] = t.strftime('%H:%M:%S')
        trips.append(trip)
    return trips


def main():
    pass


if __name__ == '__main__':
    main()
