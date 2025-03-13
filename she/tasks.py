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
                department_exists = Department.objects.filter(
                    code=emp["Global_Dimension_1_Code"]
                )
                if department_exists.exists():
                    department = department_exists.first()
                else:
                    department = None
                exists = Employee.objects.filter(no=emp["No"])
                if exists.exists():
                    employee = exists.first()
                    employee.name = emp["FullName"]
                    employee.department = department
                    employee.status = emp["Status"]
                    employee.employment_date = emp["Employment_Date"]
                    employee.save()
                else:
                    employee = Employee(
                        no=emp["No"],
                        name=emp["FullName"],
                        department=department,
                        status=emp["Status"],
                        employment_date=emp["Employment_Date"],
                    )
                    employee.save()
    except Exception as e:
        print(e)
