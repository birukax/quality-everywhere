from django.core.paginator import Paginator


def get_page(request, model):
    paginated = Paginator(model, 30)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    return page
