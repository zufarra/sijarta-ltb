import jwt
from django.db import connection
from django.shortcuts import redirect
from django.urls import reverse

from users.services.user_service import UserService
from users.utils.jwt_utils import verify_jwt


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
        token = request.COOKIES.get("jwt")
        user = {"is_authenticated": False}

        if not token:
            return user

        try:
            user_id, _ = verify_jwt(token)
            if user_id == "None":
                return user
            result = UserService.get_user_by_id(user_id)
            if user == None:
                user["message"] = "User not found"
                return user
        except jwt.ExpiredSignatureError:
            user["message"] = "Token expired"
            return user
        except jwt.InvalidTokenError:
            user["message"] = "Invalid token"
            return user

        user = result
        user["is_authenticated"] = True
        return user
