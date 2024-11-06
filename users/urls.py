from django.urls import path

from users.views import show_profile

app_name = "user"

urlpatterns = [path("profile/", show_profile, name="show_profile")]
