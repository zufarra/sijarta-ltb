from django.urls import path
from pekerjajasa.views import pekerjajasa_view, status_view

app_name = "pekerjajasa"

urlpatterns = [
    path("", pekerjajasa_view, name="pekerjajasa_view"),
    path("status/", status_view, name="status_view")
]
