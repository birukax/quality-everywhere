import pyodbc
import requests
from .models import Product, Customer, Machine
from decouple import config
from requests_ntlm import HttpNtlmAuth


def get_product():
    url = config("NAV_FINISHED_ITEMS")
    user = config("NAV_INSTANCE_USER")
    password = config("NAV_INSTANCE_PASSWORD")
    auth = HttpNtlmAuth(user, password)
    try:
        response = requests.get(url, auth=auth)
        if response.ok:
            data = response.json()
            for product in data["value"]:
                product = Product(
                    no=product["No"],
                    name=product["Description"],
                )
                if Product.objects.filter(no=product.no).exists():
                    pass
                else:
                    product.save()
    except Exception as e:
        print(e)


def get_customer():
    url = config("NAV_CUSTOMERS")
    user = config("NAV_INSTANCE_USER")
    password = config("NAV_INSTANCE_PASSWORD")
    auth = HttpNtlmAuth(user, password)
    try:
        response = requests.get(url, auth=auth)
        if response.ok:
            data = response.json()
            for customer in data["value"]:
                customer = Customer(
                    no=customer["No"],
                    name=customer["Name"],
                )
                if Customer.objects.filter(no=customer.no).exists():
                    pass
                else:
                    customer.save()
    except Exception as e:
        print(e)


def get_machine():
    url = config("NAV_MACHINES")
    user = config("NAV_INSTANCE_USER")
    password = config("NAV_INSTANCE_PASSWORD")
    auth = HttpNtlmAuth(user, password)
    try:
        response = requests.get(url, auth=auth)
        if response.ok:
            data = response.json()
            for machine in data["value"]:
                machine = Machine(
                    code=machine["No"],
                    name=machine["Name"],
                    type=machine["Work_Center_No"],
                )
                if Machine.objects.filter(code=machine.code).exists():
                    pass
                else:
                    machine.save()
    except Exception as e:
        print(e)
