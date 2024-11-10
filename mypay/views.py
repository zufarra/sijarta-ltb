from django.shortcuts import render

# Create your views here.
def mypay_view(request) :
    context = {
        "mypay": {
            "user": "John Doe",
            "name": "John Doe",
            "phone": "123-456-7890",
            "saldo" : 5000000
        }
    }
    return render(request, "show_mypay.html", context)

def transaksi_mypay(request) :
    context = {
        "mypay": {
            "user": "John Doe",
            "name": "John Doe",
            "phone": "123-456-7890",
            "saldo" : 5000000
        }
    }
    return render(request, "transaksi_mypay.html", context)