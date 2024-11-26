from db.utils.query_helpers import fetch_all, fetch_one


class UserService:
    @staticmethod
    def get_all_users():
        return fetch_all("SELECT * FROM users")

    @staticmethod
    def get_user_by_id(user_id):
        return fetch_one("SELECT * FROM users WHERE id = %s", [user_id])

    @staticmethod
    def get_user_by_phone_number(phone_number):
        return fetch_one("SELECT * FROM users WHERE no_hp = %s", [phone_number])
