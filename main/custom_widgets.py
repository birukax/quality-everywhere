from django_select2 import forms as s2forms
from assessment.models import Test, Conformity, SemiWaste
from job.models import Job, JobTest
from product.models import Product, Artwork
from misc.models import ColorStandard, Color, Customer, RawMaterial, Shift
from machine.models import Machine, Route
from issue.models import Department, Location, Issue, IssueType
from django.contrib.auth.models import User


class ArtworkWidget(s2forms.ModelSelect2Widget):
    queryset = Artwork.objects.all()
    search_fields = [
        "code__icontains",
    ]


class ColorWidget(s2forms.ModelSelect2Widget):
    queryset = Color.objects.all()
    search_fields = [
        "name__icontains",
        "code__icontains",
    ]


class ColorStandardWidget(s2forms.ModelSelect2Widget):
    queryset = ColorStandard.objects.all()
    search_fields = [
        "name__icontains",
    ]


class ConformityWidget(s2forms.ModelSelect2Widget):
    queryset = Conformity.objects.all()
    search_fields = [
        "name__icontains",
    ]


class CustomerWidget(s2forms.ModelSelect2Widget):
    queryset = Customer.objects.all()
    search_fields = [
        "no__icontains",
        "name__icontains",
    ]


class DepartmentWidget(s2forms.ModelSelect2Widget):
    queryset = Department.objects.all()
    # queryset = Department.objects.filter(active=True)
    search_fields = [
        "name__icontains",
    ]


class IssueWidget(s2forms.ModelSelect2Widget):
    queryset = Issue.objects.all()
    search_fields = [
        "id__icontains",
    ]


class IssueTypeWidget(s2forms.ModelSelect2Widget):
    queryset = IssueType.objects.all()
    # queryset = IssueType.objects.filter(active=True)
    search_fields = [
        "name__icontains",
    ]


class JobWidget(s2forms.ModelSelect2Widget):
    queryset = Job.objects.all()
    search_fields = [
        "no__icontains",
    ]


class JobTestWidget(s2forms.ModelSelect2Widget):
    queryset = JobTest.objects.all()
    search_fields = [
        "id__icontains",
    ]


class LocationWidget(s2forms.ModelSelect2Widget):
    queryset = Location.objects.all()
    # queryset = Location.objects.filter(active=True)
    search_fields = [
        "name__icontains",
    ]


class MachineWidget(s2forms.ModelSelect2Widget):
    queryset = Machine.objects.all()
    search_fields = [
        "name__icontains",
    ]


class ProductWidget(s2forms.ModelSelect2Widget):
    queryset = Product.objects.all()
    search_fields = [
        "no__icontains",
        "name__icontains",
    ]


class RouteWidget(s2forms.ModelSelect2Widget):
    queryset = Route.objects.all()
    search_fields = [
        "name__icontains",
    ]


class RawMaterialWidget(s2forms.ModelSelect2Widget):
    queryset = RawMaterial.objects.all()
    search_fields = [
        "no__icontains",
        "name__icontains",
    ]


class SemiWasteWidget(s2forms.ModelSelect2Widget):
    queryset = SemiWaste.objects.all()
    search_fields = [
        "tag_no__icontains",
    ]


class ShiftWidget(s2forms.ModelSelect2Widget):
    queryset = Shift.objects.all()
    search_fields = [
        "name__icontains",
        "code__icontains",
    ]


class TestWidget(s2forms.ModelSelect2Widget):
    model = Test
    search_fields = [
        "name__icontains",
    ]


class UserWidget(s2forms.ModelSelect2Widget):
    queryset = User.objects.all()
    search_fields = [
        "username__icontains",
    ]
