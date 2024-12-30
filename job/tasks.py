import requests
from .models import Job
from decouple import config
from requests_ntlm import HttpNtlmAuth
from misc.models import Product


def get_job():
    url = config("NAV_ORDERS")
    user = config("NAV_INSTANCE_USER")
    password = config("NAV_INSTANCE_PASSWORD")
    auth = HttpNtlmAuth(user, password)
    try:
        response = requests.get(url, auth=auth)
        if response.ok:
            data = response.json()
            for job in data["value"]:
                job = Job(
                    no=job["No"],
                    product=Product.objects.get(no=job["Source_No"]),
                )
                job_exists = Job.objects.filter(no=job.no)
                product_exists = Product.objects.filter(no=job.product.no)
                if product_exists.exists():
                    if job_exists.exists():
                        job_exists.update(
                            product=Product.objects.get(no=job.product.no),
                        )
                    else:
                        job.save()
    except Exception as e:
        print(e)


def get_customer():
    pass


def create_first_offs(job_no):
    pass
