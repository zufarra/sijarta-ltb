from django.db import connection


def execute_query(sql, params=None):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)


def fetch_all(sql, params=None):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        return cursor.fetchall()


def fetch_one(sql, params=None):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        return cursor.fetchone()
