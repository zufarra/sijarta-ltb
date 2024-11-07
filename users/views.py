from django.shortcuts import render

# Create your views here.


def show_landing(request):
    return render(request, "show_landing.html")


def show_profile(request):
    context = {
        "user": {
            "is_authenticated": True,
            "name": "John Doe",
            "is_pengguna": True,
            "email": "johndoe@mail.com",
            "phone": "123-456-7890",
            "address": "1234 Elm St",
        }
    }

    return render(request, "show_profile.html", context)


def show_login(request):
    context = {
        "user": {
            "is_authenticated": True,
            "name": "John Doe",
            "is_pengguna": True,
            "email": "johndoe@mail.com",
            "phone": "123-456-7890",
            "address": "1234 Elm St",
        }
    }

    return render(request, "show_login.html", context)


def show_register(request):
    context = {
        "user": {
            "is_authenticated": True,
            "name": "John Doe",
            "is_pengguna": True,
            "email": "johndoe@mail.com",
            "phone": "123-456-7890",
            "address": "1234 Elm St",
        }
    }

    return render(request, "show_register.html", context)
