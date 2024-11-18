from django.shortcuts import redirect
from django.urls import reverse


class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = self.authenticate_user(request)

        exempt_urls = [
            reverse("user:show_landing"),
            reverse("user:show_login"),
            reverse("user:show_register"),
        ]

        if not user["is_authenticated"] and request.path not in exempt_urls:
            return redirect("user:show_landing")

        request.user = user

        return self.get_response(request)

    def authenticate_user(self, request):
        return {
            "is_authenticated": False,
            "name": "John Doe",
            "is_pengguna": True,
            "email": "johndoe@mail.com",
            "phone": "123-456-7890",
            "address": "1234 Elm St",
        }
