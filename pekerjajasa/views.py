from django.shortcuts import render
from django.http import HttpResponse

def pekerjajasa_view(request) :
    context = {
        "user": {
            "is_authenticated": True,
            "name": "Powder",
            "is_pengguna": False,
            "email": "johndoe@mail.com",
            "phone": "123-456-7890",
            "address": "1234 Elm St",
        }
    }
    if context['user']['is_pengguna']: 
       return HttpResponse('Unauthorized', status=401)
    return render(request, "show_pekerjajasa.html", context)

def status_view(request) :
    context = {
        "user": {
            "is_authenticated": True,
            "name": "Powder",
            "is_pengguna": False,
            "email": "johndoe@mail.com",
            "phone": "123-456-7890",
            "address": "1234 Elm St",
        }
    }
    if context['user']['is_pengguna']: 
        return HttpResponse('Unauthorized', status=401)
    return render(request, "show_status.html", context)
