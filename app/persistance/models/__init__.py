from app.persistance.db import Document, db


class User(Document):
    collection = db.users


class Trip(Document):
    collection = db.trips
