
from app.persistance.models import Trip


def get_all_trips():
    trips = Trip.all()
    return trips
