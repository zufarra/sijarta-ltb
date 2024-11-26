from django.db import connection
from django.shortcuts import redirect
from django.urls import reverse


class AuthorizationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/__reload__"):
            return self.get_response(request)

        user = self.authenticate_user(request)

        exempt_urls = [
            reverse("user:show_landing"),
            reverse("user:show_login"),
            reverse("user:register"),
        ]

        if not user["is_authenticated"] and request.path not in exempt_urls:
            return redirect("user:show_landing")

        request.user = user

        return self.get_response(request)

    def authenticate_user(self, request):
        token = request.headers.get("Authorization")
        if token:
            token = token.split(" ")[1]
            user_id, username = self.verify_jwt(token)

            if user_id:
                return self.get_user_from_db(user_id, username)

        return {"is_authenticated": False}

    def get_user_from_db(self, user_id, username):
        sql = "SELECT * FROM sijarta.user WHERE id = %s AND name = %s"

        with connection.cursor() as cursor:
            cursor.execute(sql, [user_id, username])
            row = cursor.fetchone()

        if row:
            return {"is_authenticated": True, "id": row[0], "name": row[1]}
        return {"is_authenticated": False}
