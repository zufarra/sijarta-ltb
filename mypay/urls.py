from django.urls import path
from mypay.views import mypay_view, transaksi_mypay

app_name = "mypay"

urlpatterns = [
    path("", mypay_view, name="mypay_view"),
    path("transaksi/", transaksi_mypay, name="transaksi_mypay"),
]
