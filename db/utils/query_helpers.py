from typing import Any, Dict, List, Optional, Tuple

from django.db import connection, transaction


def execute_query(sql: str, params: Optional[List[Any]] = None) -> None:
    """
    Execute a SQL query (INSERT, UPDATE, DELETE)
    Uses transaction.atomic() for safety
    """
    with transaction.atomic():
        with connection.cursor() as cursor:
            cursor.execute(sql, params)


def fetch_all(sql: str, params: Optional[List[Any]] = None) -> List[Tuple]:
    """
    Fetch all rows from a query
    Returns raw tuples
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        return cursor.fetchall()


def fetch_one(sql: str, params: Optional[List[Any]] = None) -> Optional[Tuple]:
    """
    Fetch a single row from a query
    Returns raw tuple or None
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        return cursor.fetchone()


def fetch_dict_all(
    sql: str, params: Optional[List[Any]] = None
) -> List[Dict[str, Any]]:
    """
    Fetch all rows and return as list of dictionaries
    Adds column names to the results
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def fetch_dict_one(
    sql: str, params: Optional[List[Any]] = None
) -> Optional[Dict[str, Any]]:
    """
    Fetch a single row and return as dictionary
    Adds column names to the result
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, params)

        # If no results, return None
        result = cursor.fetchone()
        if not result:
            return None

        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, result))
