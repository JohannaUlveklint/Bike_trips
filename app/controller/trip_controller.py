import datetime

from app.persistance.repository import trip_repo


def get_all_trips():
    trips_db = trip_repo.get_all_trips()
    base_date = datetime.datetime(1, 1, 1, 0, 0, 0, 0)
    # [setattr(trip, 'time', base_date + datetime.timedelta(seconds=trip.duration)) for trip in trips_db]
    trips = []
    for trip in trips_db:
        t = base_date + datetime.timedelta(seconds=trip.duration)
        trip.time = t.strftime('%H:%M:%S')
        trips.append(trip)
    return trips


def main():
    trips = get_all_trips()
    print()


if __name__ == '__main__':
    main()


