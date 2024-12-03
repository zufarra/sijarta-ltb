from django.http import HttpResponse
from django.shortcuts import render
from pekerjajasa.services.pekerjajasa_servise import PekerjaJasaService


def pekerjajasa_view(request):
    if request.user["is_pengguna"]:
        return HttpResponse("Unauthorized", status=401)

    context = {
        "user": request.user,
    }
    return render(request, "show_pekerjajasa.html", context)


def status_view(request):
    pekerja_id = str(request.user['id'])
    pekerjaan = PekerjaJasaService.get_tr_pemesanan_jasa_by_pekerja(pekerja_id)
    context = {
        "user": request.user,
        "pekerjaan" : pekerjaan
    }
    if context["user"]["is_pengguna"]:
        return HttpResponse("Unauthorized", status=401)
    return render(request, "show_status.html", context)
