from django.http import HttpResponse
from django.shortcuts import render


def pekerjajasa_view(request):
    context = {
        "user": request.user,
    }
    if context["user"]["is_pengguna"]:
        return HttpResponse("Unauthorized", status=401)
    return render(request, "show_pekerjajasa.html", context)


def status_view(request):
    context = {
        "user": request.user,
    }
    if context["user"]["is_pengguna"]:
        return HttpResponse("Unauthorized", status=401)
    return render(request, "show_status.html", context)
