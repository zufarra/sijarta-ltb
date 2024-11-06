from django.shortcuts import render

# Create your views here.


def show_landing(request):
    return render(request, "show_landing.html")


def show_profile(request):
    context = {"name": "John Doe", "email": "johndoe@email.com"}

    return render(request, "show_profile.html", context)


def show_login(request):
    context = {"name": "John Doe", "email": "johndoe@email.com"}

    return render(request, "show_login.html", context)


def show_register(request):
    context = {"name": "John Doe", "email": "johndoe@email.com"}

    return render(request, "show_register.html", context)
