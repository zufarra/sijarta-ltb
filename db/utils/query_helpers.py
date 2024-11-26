from django.db import connection, transaction


def execute_query(sql, params=None):
    with transaction.atomic():
        with connection.cursor() as cursor:
            cursor.execute(sql, params)


def fetch_all(sql, params=None):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def fetch_one(sql, params=None):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            print(columns)
            print(row)
            return dict(zip(columns, row))
        return None
