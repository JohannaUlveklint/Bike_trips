from app.persistance.repository import user_repo


def get_all_users():
    return user_repo.get_all_users()