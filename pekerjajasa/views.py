from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
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
    statuses = PekerjaJasaService.get_statuses_for_pekerja()
    match = None
    status = None

    if request.method == "POST" :
        match = request.POST.get("match")    
        status = request.POST.get("status")

    pekerjaan = PekerjaJasaService.get_tr_pemesanan_jasa_by_pekerja(pekerja_id, match, status)

    context = {
        "user": request.user,
        "pekerjaan" : pekerjaan,
        'statuses' : statuses
    }
    if context["user"]["is_pengguna"]:
        return HttpResponse("Unauthorized", status=401)
    return render(request, "show_status.html", context)


def update_status(request):
    if request.method == "POST" :
        id_pemesanan = str(request.POST.get("id"))
        PekerjaJasaService.update_status(id_pemesanan)
        return redirect('pekerjajasa:status_view')
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

