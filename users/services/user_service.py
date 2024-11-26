import uuid

import bcrypt

from db.utils.query_helpers import execute_query, fetch_all, fetch_one


class UserService:
    user_columns = ["id", "nama", "jenis_kelamin", "no_hp", "tgl_lahir", "alamat"]

    @staticmethod
    def get_all_users():
        """Gets all users from the database."""
        return fetch_all("SELECT * FROM sijarta.user")

    @staticmethod
    def get_user_by_id(user_id: uuid.UUID):
        """Gets a user by ID from the database"""
        return fetch_one("SELECT * FROM sijarta.user WHERE id = %s", [user_id])

    @staticmethod
    def get_user_by_phone_number(phone_number: str) -> dict:
        """Gets a user by phone number from the database."""
        row = fetch_one("SELECT * FROM sijarta.user WHERE no_hp = %s", [phone_number])
        return dict(zip(UserService.user_columns, row)) if row else None

    @staticmethod
    def hash_password(password):
        """Hashes the given password."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt)

    @staticmethod
    def create_pengguna(name, password, gender, phone_number, birthdate, address):
        """Creates a new pengguna in the database."""
        id = uuid.uuid4()
        sql = """
        INSERT INTO sijarta.user (id, nama, jenis_kelamin, no_hp, pwd, tgl_lahir, alamat, saldo_mypay)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 0)
        """

        hashed_password = UserService.hash_password(password)
        execute_query(
            sql,
            [
                id,
                name,
                gender,
                phone_number,
                hashed_password.decode("utf-8"),
                birthdate,
                address,
            ],
        )
