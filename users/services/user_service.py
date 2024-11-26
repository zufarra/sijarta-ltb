import uuid

from django.contrib.auth.hashers import check_password, make_password

from db.utils.query_helpers import execute_query, fetch_dict_all, fetch_dict_one


class UserService:
    USER_FIELDS = """
        U.id as id,
        U.nama as name,
        U.jenis_kelamin as gender,
        U.no_hp as phone_number,
        U.pwd as password_hash,
        U.tgl_lahir as birthdate,
        U.alamat as address,
        U.saldo_mypay as mypay_balance,
        P.level as level,
        PE.nama_bank as bank_name,
        PE.nomor_rekening as bank_account_number,
        PE.npwp as npwp,
        PE.link_foto as photo_url,
        PE.rating as rating,
        PE.jml_pesanan_selesai as jml_pesanan_selesai
    """

    @staticmethod
    def get_all_users():
        """Gets all users from the database."""
        sql = f"""
        SELECT
            {UserService.USER_FIELDS}
        FROM sijarta.user U
        LEFT JOIN sijarta.pelanggan P ON U.id = P.id
        LEFT JOIN sijarta.pekerja PE ON U.id = PE.id;
        """

        return fetch_dict_all(sql)

    @staticmethod
    def get_user_by_id(user_id: uuid.UUID):
        """Gets a user by ID from the database"""
        sql = f"""
        SELECT 
            {UserService.USER_FIELDS}
        FROM sijarta.user U
        LEFT JOIN sijarta.pelanggan P ON U.id = P.id
        LEFT JOIN sijarta.pekerja PE ON U.id = PE.id
        WHERE U.id = %s;
        """

        result = fetch_dict_one(sql, [user_id])
        if not result:
            return None

        level = result.get("level")

        if not level:
            result["is_pengguna"] = False
        else:
            result["is_pengguna"] = True

        return result

    @staticmethod
    def get_user_by_phone_number(phone_number: str) -> dict:
        """Gets a user by phone number from the database."""
        sql = f"""
        SELECT
            {UserService.USER_FIELDS}
        FROM sijarta.user U
        LEFT JOIN sijarta.pelanggan P ON U.id = P.id
        LEFT JOIN sijarta.pekerja PE ON U.id = PE.id
        WHERE U.no_hp = %s;
        """

        result = fetch_dict_one(sql, [phone_number])
        if not result:
            return None

        level = result.get("level")

        if not level:
            result["is_pengguna"] = False
        else:
            result["is_pengguna"] = True

        return result

    @staticmethod
    def hash_password(password):
        """Hashes the given password."""
        return make_password(password)

    @staticmethod
    def check_password(password, hashed_password):
        """Checks if the given password matches the hashed password."""
        return check_password(password, hashed_password)

    @staticmethod
    def create_pengguna(name, password, gender, phone_number, birthdate, address):
        """Creates a new pengguna in the database."""
        id = uuid.uuid4()
        level = "Basic"
        sql = """
        INSERT INTO sijarta.user (id, nama, jenis_kelamin, no_hp, pwd, tgl_lahir, alamat, saldo_mypay)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 0);

        INSERT INTO sijarta.pelanggan (id, level)
        VALUES (%s, %s);
        """

        hashed_password = UserService.hash_password(password)
        execute_query(
            sql,
            [
                id,
                name,
                gender,
                phone_number,
                hashed_password,
                birthdate,
                address,
                id,
                level,
            ],
        )

    @staticmethod
    def create_pekerja(
        name,
        password,
        gender,
        phone_number,
        birthdate,
        address,
        bank_name,
        bank_account_number,
        npwp,
        photo_url,
    ):
        """Creates a new pekerja in the database."""
        id = uuid.uuid4()
        # Untuk rating asumsi NULL jika belum ada pesanan yang diselesaikan
        # Untuk jml_pesanan_selesai asumsi 0 jika belum ada pesanan yang diselesaikan
        sql = """
        INSERT INTO sijarta.user (id, nama, jenis_kelamin, no_hp, pwd, tgl_lahir, alamat, saldo_mypay)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 0);

        INSERT INTO sijarta.pekerja (id, nama_bank, nomor_rekening, npwp, link_foto, rating, jml_pesanan_selesai)
        VALUES (%s, %s, %s, %s, %s, NULL, 0);
        """

        hashed_password = UserService.hash_password(password)
        execute_query(
            sql,
            [
                id,
                name,
                gender,
                phone_number,
                hashed_password,
                birthdate,
                address,
                id,
                bank_name,
                bank_account_number,
                npwp,
                photo_url,
            ],
        )

    @staticmethod
    def update_pengguna(id, name, password, gender, phone_number, birthdate, address):
        """Updates a pengguna in the database."""
        sql = """
        UPDATE sijarta.user
        SET nama = %s, jenis_kelamin = %s, no_hp = %s, pwd = %s, tgl_lahir = %s, alamat = %s
        WHERE id = %s;
        """

        hashed_password = UserService.hash_password(password)
        execute_query(
            sql,
            [name, gender, phone_number, hashed_password, birthdate, address, id],
        )
