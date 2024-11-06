from django.shortcuts import render

# Create your views here.


def show_profile(request):

    context = {"name": "John Doe", "email": "johndoe@email.com"}

    return render(request, "show_profile.html", context)
