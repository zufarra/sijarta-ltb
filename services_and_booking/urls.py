from django.urls import path
from services_and_booking.views import show_homepage, show_subkategori,show_booking_view, create_testimoni

#from users.views import 

app_name = "service"

urlpatterns = [
    path("homepage/", show_homepage, name="show_homepage"),
    path("subkategori/", show_subkategori, name="show_subkategori"),
    path("booking_view/", show_booking_view, name="show_booking_view"),
    path("create_testimoni/", create_testimoni, name="create_testimoni")
    
]