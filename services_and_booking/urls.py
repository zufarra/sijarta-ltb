from django.urls import path
from services_and_booking.views import show_homepage, show_subkategori,show_booking_view,search_subcategory

#from users.views import 

app_name = "service"

urlpatterns = [
    path("homepage/", show_homepage, name="show_homepage"),
    path('search-subcategory/', search_subcategory, name='search_subcategory'),
    path("subkategori/", show_subkategori, name="show_subkategori"),
    path("booking_view/", show_booking_view, name="show_booking_view")
]