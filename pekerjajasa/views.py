from django.shortcuts import render

def pekerjajasa_view(request) :
    context = {}
    return render(request, "show_pekerjajasa.html", context)

def status_view(request) :
    context = {}
    return render(request, "show_status.html", context)
