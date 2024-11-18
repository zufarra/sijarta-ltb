from django.urls import path

from diskon.views import show_diskon

app_name = "diskon"

urlpatterns = [
    path('', show_diskon, name="show_diskon"),
]
