import requests
from .models import Department, Employee
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
                department, updated = Department.objects.filter(
                    code=dept["Code"]
                ).update_or_create(
                    code=dept["Code"],
                    name=dept["Name"],
                )
        else:
            print(response.status_code, response.reason)
    except Exception as e:
        print(e)


def employees_get():
    url = config("NAV_EMPLOYEES")
    user = config("NAV_INSTANCE_USER")
    password = config("NAV_INSTANCE_PASSWORD")
    auth = HttpNtlmAuth(user, password)
    try:
        response = requests.get(url, auth=auth)
        if response.ok:
            data = response.json()
            departments_get()
            for emp in data["value"]:
                department = Department.objects.filter(
                    code=emp["Global_Dimension_1_Code"]
                )
                if department.exists():
                    department = department.first()
                else:
                    department = None
                employee, updated = Employee.objects.filter(
                    no=emp["No"]
                ).update_or_create(
                    no=emp["No"],
                    name=emp["FullName"],
                    department=department,
                    status=emp["Status"],
                    employment_date=emp["Employment_Date"],
                )
        else:
            print(response.status_code, response.reason)
    except Exception as e:
        print(e)
