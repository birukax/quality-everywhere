from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from misc.tasks import get_product, get_customer, get_machine
from job.tasks import get_job


@login_required
def dashboard(request):
    get_product()
    get_customer()
    get_job()
    # get_machine()
    return render(request, "dashboard.html")
