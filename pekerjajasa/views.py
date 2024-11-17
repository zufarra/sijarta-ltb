from django.shortcuts import render

def pekerjajasa_view(request) :
    context = {
        "user": {
            "is_authenticated": True,
            "name": "John Doe",
            "is_pengguna": False,
            "email": "johndoe@mail.com",
            "phone": "123-456-7890",
            "address": "1234 Elm St",
        }
    }
    return render(request, "show_pekerjajasa.html", context)

def status_view(request) :
    context = {
        "user": {
            "is_authenticated": True,
            "name": "John Doe",
            "is_pengguna": False,
            "email": "johndoe@mail.com",
            "phone": "123-456-7890",
            "address": "1234 Elm St",
        }
    }
    return render(request, "show_status.html", context)
