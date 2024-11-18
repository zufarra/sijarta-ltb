from django.shortcuts import render

# Create your views here.
def mypay_view(request) :
    context = {
        "user": {
            "is_authenticated": True,
            "name": "Vander",
            "is_pengguna": False,
            "email": "johndoe@mail.com",
            "phone": "123-456-7890",
            "address": "1234 Elm St",
        }
    }
    return render(request, "show_mypay.html", context)

def transaksi_mypay(request) :
    context = {
        "user": {
            "is_authenticated": True,
            "name": "Vander",
            "is_pengguna": False,
            "email": "johndoe@mail.com",
            "phone": "123-456-7890",
            "address": "1234 Elm St",
        }
    }
    return render(request, "transaksi_mypay.html", context)