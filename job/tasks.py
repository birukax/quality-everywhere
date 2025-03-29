import requests
from django.shortcuts import get_object_or_404
from assessment.models import Assessment
from assessment.models import FirstOff
from .models import Job
from decouple import config
from requests_ntlm import HttpNtlmAuth
from product.models import Product


def job_get():
    url = config("NAV_ORDERS")
    user = config("NAV_INSTANCE_USER")
    password = config("NAV_INSTANCE_PASSWORD")
    auth = HttpNtlmAuth(user, password)
    # try:
    response = requests.get(url, auth=auth)
    if response.ok:
        data = response.json()
        for job in data["value"]:
            product = Product.objects.filter(no=job["Source_No"])
            if product.exists():
                job, updated = Job.objects.filter(no=job["No"]).update_or_create(
                        no=job["No"],
                        product=product.first(),
                )
    # except Exception as e:
    #     print(e)


# def create_assessments(request, id):
#     job = get_object_or_404(Job, id=id)
#     if request.method == "POST":
#         form = CreateFirstOffForm(request.POST)
#         if form.is_valid():
#             machines = form.cleaned_data["machines"]
#             for machine in machines:
#                 assessment = QualityTest(
#                     job=job,
#                     machine=machine,
#                     no=job.tests,
#                     created_by=request.user,
#                 )
#                 assessment.save()
#                 for t in machine.tests.all():
#                     test = FirstOff(
#                         assessment=assessment,
#                         test=t,
#                     )
#                     test.save()
#             job.tests = job.tests + 1
#             job.save()
