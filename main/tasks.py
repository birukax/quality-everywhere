from django.core.paginator import Paginator
from django.shortcuts import render


def get_page(request, model):
    paginated = Paginator(model, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    return page


def role_check(allowed_roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if (
                request.user.is_authenticated
                and request.user.profile.role in allowed_roles
            ) or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, "registration/403.html")

        return wrapper

    return decorator
