from app.persistance.db import Document, db


class User(Document):
    collection = db.users

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email


# class Trip(Document):
#     collection = db.trips


class Route(Document):
    pass
