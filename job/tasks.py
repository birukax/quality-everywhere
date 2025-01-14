import requests
from django.shortcuts import get_object_or_404
from quality_test.models import QualityTest
from assesment.models import FirstOff
from .models import Job
from decouple import config
from requests_ntlm import HttpNtlmAuth
from misc.models import Product


def job_get():
    url = config("NAV_ORDERS")
    user = config("NAV_INSTANCE_USER")
    password = config("NAV_INSTANCE_PASSWORD")
    auth = HttpNtlmAuth(user, password)
    try:
        response = requests.get(url, auth=auth)
        if response.ok:
            data = response.json()
            for job in data["value"]:
                product = Product.objects.filter(no=job["Source_No"])
                if product.exists():
                    job = Job(
                        no=job["No"],
                        product=product.first(),
                    )
                    job_exists = Job.objects.filter(no=job.no)
                    if job_exists.exists():
                        job_exists.update(
                            product=Product.objects.get(no=job.product.no),
                        )
                    else:
                        job.save()
    except Exception as e:
        print(e)


# def create_quality_tests(request, id):
#     job = get_object_or_404(Job, id=id)
#     if request.method == "POST":
#         form = CreateFirstOffForm(request.POST)
#         if form.is_valid():
#             machines = form.cleaned_data["machines"]
#             for machine in machines:
#                 quality_test = QualityTest(
#                     job=job,
#                     machine=machine,
#                     no=job.tests,
#                     created_by=request.user,
#                 )
#                 quality_test.save()
#                 for t in machine.tests.all():
#                     test = FirstOff(
#                         quality_test=quality_test,
#                         test=t,
#                     )
#                     test.save()
#             job.tests = job.tests + 1
#             job.save()
