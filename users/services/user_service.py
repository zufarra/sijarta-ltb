from db.utils import execute_query, fetch_all, fetch_one


class UserService:
    @staticmethod
    def get_all_users():
        return fetch_all("SELECT * FROM users")

    @staticmethod
    def get_user_by_id(user_id):
        return fetch_one("SELECT * FROM users WHERE id = %s", [user_id])
