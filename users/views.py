from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from users.forms import PekerjaRegistrationForm, PenggunaRegistrationForm

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


@csrf_exempt
def register(request):
    pengguna_form = PenggunaRegistrationForm()
    pekerja_form = PekerjaRegistrationForm()
    if request.method == "POST":
        # Register user
        if request.POST["user_type"] == "pengguna":
            # Register pengguna
            pengguna_form = PenggunaRegistrationForm(request.POST)
            if not pengguna_form.is_valid():
                return render(
                    request,
                    "show_register.html",
                    {"pengguna_form": pengguna_form, "pekerja_form": pekerja_form},
                )
            name = request.POST["name"]
            password = request.POST["password"]
            gender = request.POST["gender"]
            phone_number = request.POST["phone"]
            birthdate = request.POST["birthdate"]
            address = request.POST["address"]

            pass
        elif request.POST["user_type"] == "pekerja":
            # Register pekerja
            pekerja_form = PekerjaRegistrationForm(request.POST)
            if not pekerja_form.is_valid():
                return render(
                    request,
                    "show_register.html",
                    {"pengguna_form": pengguna_form, "pekerja_form": pekerja_form},
                )

            name = request.POST["name"]
            password = request.POST["password"]
            gender = request.POST["gender"]
            phone_number = request.POST["phone"]
            birthdate = request.POST["birthdate"]
            address = request.POST["address"]
            bank_name = request.POST["bank_name"]
            bank_account = request.POST["bank_account"]
            npwp = request.POST["npwp"]
            photo_url = request.POST["photo_url"]
            pass
        else:
            return HttpResponse("Invalid user type", status=400)

    return render(
        request,
        "show_register.html",
        {"pengguna_form": pengguna_form, "pekerja_form": pekerja_form},
    )
