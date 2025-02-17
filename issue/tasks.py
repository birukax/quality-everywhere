import requests
from .models import Department
from decouple import config
from requests_ntlm import HttpNtlmAuth


def departments_get():
    url = config("NAV_DEPARTMENTS")
    user = config("NAV_INSTANCE_USER")
    password = config("NAV_INSTANCE_PASSWORD")
    auth = HttpNtlmAuth(user, password)

    try:
        response = requests.get(url, auth=auth)
        if response.ok:
            data = response.json()
            for dept in data["value"]:
                exists = Department.objects.filter(code=dept["Code"])
                if exists.exists():
                    exists = exists.first()
                    exists.department = dept["Name"]
                    exists.save()
                else:
                    department = Department(
                        code=dept["Code"],
                        name=dept["Name"],
                    )
                    department.save()
        else:
            print(response.status_code, response.reason)
    except Exception as e:
        print(e)
