import requests
from .models import Product
from decouple import config
from requests_ntlm import HttpNtlmAuth


def product_get():
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
