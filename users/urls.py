from django.urls import path

from users.views import show_landing, show_login, show_profile, show_register

app_name = "user"

urlpatterns = [
    path("", show_landing, name="show_landing"),
    path("profile/", show_profile, name="show_profile"),
    path("login/", show_login, name="show_login"),
    path("register/", show_register, name="show_register"),
]
