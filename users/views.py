from django.http import JsonResponse
from django.shortcuts import redirect, render

from users.forms import PekerjaRegistrationForm, PenggunaRegistrationForm, UserLoginForm
from users.services.user_service import UserService
from users.utils.jwt_utils import generate_jwt

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
    login_form = UserLoginForm()
    context = {
        "form": login_form,
    }

    return render(request, "show_login.html", context)


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
                    {
                        "pengguna_form": pengguna_form,
                        "pekerja_form": pekerja_form,
                    },
                )

            name = request.POST["name"]
            password = request.POST["password"]
            gender = request.POST["gender"]
            phone_number = request.POST["phone_number"]
            birthdate = request.POST["birthdate"]
            address = request.POST["address"]

            search_phone_number = UserService.get_user_by_phone_number(phone_number)
            if search_phone_number:
                return JsonResponse(
                    {"message": "Phone number already registered"}, status=400
                )

            gender = "L" if gender == "M" else "P"

            try:
                UserService.create_pengguna(
                    name, password, gender, phone_number, birthdate, address
                )
            except Exception as e:
                return JsonResponse(
                    {"message": "Failed to register user", "error": str(e)}, status=500
                )

            return redirect("user:show_login")
        elif request.POST["user_type"] == "pekerja":
            # Register pekerja
            pekerja_form = PekerjaRegistrationForm(request.POST)
            if not pekerja_form.is_valid():
                return render(
                    request,
                    "show_register.html",
                    {
                        "pengguna_form": pengguna_form,
                        "pekerja_form": pekerja_form,
                        "show_pekerja": True,
                    },
                )

            name = request.POST["name"]
            password = request.POST["password"]
            gender = request.POST["gender"]
            phone_number = request.POST["phone_number"]
            birthdate = request.POST["birthdate"]
            address = request.POST["address"]
            bank_name = request.POST["bank_name"]
            bank_account_number = request.POST["bank_account_number"]
            npwp = request.POST["npwp"]
            photo_url = request.POST["photo_url"]

            search_phone_number = UserService.get_user_by_phone_number(phone_number)
            if search_phone_number:
                return JsonResponse(
                    {"message": "Phone number already registered"}, status=400
                )

            gender = "L" if gender == "M" else "P"

            try:
                UserService.create_pekerja(
                    name,
                    password,
                    gender,
                    phone_number,
                    birthdate,
                    address,
                    bank_name,
                    bank_account_number,
                    npwp,
                    photo_url,
                )
            except Exception as e:
                return JsonResponse(
                    {"message": "Failed to register user", "error": str(e)}, status=500
                )

            return redirect("user:show_login")
        else:
            return JsonResponse({"message": "Invalid user type"}, status=400)

    return render(
        request,
        "show_register.html",
        {"pengguna_form": pengguna_form, "pekerja_form": pekerja_form},
    )
