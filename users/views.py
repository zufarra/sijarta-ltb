from django.shortcuts import redirect, render

# Create your views here.


def show_landing(request):
    context = {
        "user": request.user,
    }
    if not context["user"]["is_authenticated"]:
        return render(request, "show_landing.html")

    return redirect("service:show_homepage")


def show_profile(request):
    context = {
        "user": request.user,
    }

    return render(request, "show_profile.html", context)


def show_login(request):
    context = {
        "user": request.user,
    }

    return render(request, "show_login.html", context)


def show_register(request):
    context = {
        "user": request.user,
    }

    return render(request, "show_register.html", context)
