from django.shortcuts import render


# Create your views here.
def mypay_view(request):
    context = {"user": request.user}
    return render(request, "show_mypay.html", context)


def transaksi_mypay(request):
    context = {"user": request.user}
    return render(request, "transaksi_mypay.html", context)

