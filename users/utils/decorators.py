from django.http import HttpResponseRedirect
from django.urls import reverse


def only_pengguna(view_func=None, redirect_url=None):
    """Decorator to check if the user is authenticated and a pengguna."""

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user["is_authenticated"]:
                return HttpResponseRedirect(reverse("user:show_login"))
            if not request.user["is_pengguna"]:
                return HttpResponseRedirect(
                    redirect_url or reverse("user:show_landing")
                )
            return view_func(request, *args, **kwargs)

        return wrapper

    if view_func:
        return decorator(view_func)
    return decorator


def only_pekerja(view_func=None, redirect_url=None):
    """Decorator to check if the user is authenticated and a pekerja."""

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user["is_authenticated"]:
                return HttpResponseRedirect(reverse("user:show_login"))
            if request.user["is_pengguna"]:
                return HttpResponseRedirect(
                    redirect_url or reverse("user:show_landing")
                )
            return view_func(request, *args, **kwargs)

        return wrapper

    if view_func:
        return decorator(view_func)
    return decorator
