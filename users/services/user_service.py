import uuid

from django.contrib.auth.hashers import check_password, make_password

from db.utils.query_helpers import execute_query, fetch_all, fetch_one


class UserService:
    user_columns = [
        "id",
        "nama",
        "jenis_kelamin",
        "no_hp",
        "pwd",
        "tgl_lahir",
        "alamat",
    ]

    @staticmethod
    def get_all_users():
        """Gets all users from the database."""
        return fetch_all("SELECT * FROM sijarta.user")

    @staticmethod
    def get_user_by_id(user_id: uuid.UUID):
        """Gets a user by ID from the database"""
        pengguna_sql = """
        SELECT (U.id, U.nama, U.jenis_kelamin, U.no_hp, U.pwd, U.tgl_lahir, U.alamat, U.saldo_mypay, P.level)
        FROM sijarta.user U
        RIGHT JOIN sijarta.pelanggan P ON U.id = P.id
        WHERE U.id = %s;
        """

        pekerja_sql = """
        SELECT (U.id, U.nama, U.jenis_kelamin, U.no_hp, U.pwd, U.tgl_lahir, U.alamat, U.saldo_mypay, P.nama_bank, P.nomor_rekening, P.npwp, P.link_foto, P.rating, P.jml_pesanan_selesai)
        FROM sijarta.user U
        RIGHT JOIN sijarta.pekerja P ON U.id = P.id
        WHERE U.id = %s;
        """

        pengguna_row = fetch_one(pengguna_sql, [user_id])
        pekerja_row = fetch_one(pekerja_sql, [user_id])

        if pengguna_row:
            pengguna_row = tuple(pengguna_row[0][1:-1].split(","))
            return {
                "is_pengguna": True,
                "id": pengguna_row[0],
                "nama": pengguna_row[1],
                "jenis_kelamin": pengguna_row[2],
                "no_hp": pengguna_row[3],
                "pwd": pengguna_row[4],
                "tgl_lahir": pengguna_row[5],
                "alamat": pengguna_row[6],
                "saldo_mypay": pengguna_row[7],
                "level": pengguna_row[8],
            }
        elif pekerja_row:
            pekerja_row = pekerja_row[0]
            return {
                "is_pengguna": False,
                "id": pekerja_row[0],
                "nama": pekerja_row[1],
                "jenis_kelamin": pekerja_row[2],
                "no_hp": pekerja_row[3],
                "pwd": pekerja_row[4],
                "tgl_lahir": pekerja_row[5],
                "alamat": pekerja_row[6],
                "saldo_mypay": pekerja_row[7],
                "nama_bank": pekerja_row[8],
                "nomor_rekening": pekerja_row[9],
                "npwp": pekerja_row[10],
                "link_foto": pekerja_row[11],
                "rating": pekerja_row[12],
                "jml_pesanan_selesai": pekerja_row[13],
            }

        return None

    @staticmethod
    def get_user_by_phone_number(phone_number: str) -> dict:
        """Gets a user by phone number from the database."""
        row = fetch_one("SELECT * FROM sijarta.user WHERE no_hp = %s", [phone_number])
        return dict(zip(UserService.user_columns, row)) if row else None

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
