import django_filters
from django_select2 import forms as s2forms

from .models import Job, JobTest
from product.models import Product
from misc.models import ColorStandard, Customer, RawMaterial
from machine.models import Machine, Route


class JobWidget(s2forms.ModelSelect2Widget):
    queryset = Job.objects.all()
    search_fields = [
        "no__icontains",
    ]


class CustomerWidget(s2forms.ModelSelect2Widget):
    queryset = Customer.objects.all()
    search_fields = [
        "no__icontains",
        "name__icontains",
    ]


class ProductWidget(s2forms.ModelSelect2Widget):
    queryset = Product.objects.all()
    search_fields = [
        "no__icontains",
        "name__icontains",
    ]


class MachineWidget(s2forms.ModelSelect2Widget):
    queryset = Machine.objects.all()
    search_fields = [
        "name__icontains",
    ]


class RouteWidget(s2forms.ModelSelect2Widget):
    queryset = Route.objects.all()
    search_fields = [
        "name__icontains",
    ]


class ColorStandardWidget(s2forms.ModelSelect2Widget):
    queryset = ColorStandard.objects.all()
    search_fields = [
        "name__icontains",
        "name__icontains",
    ]


class RawMaterialWidget(s2forms.ModelSelect2Widget):
    queryset = RawMaterial.objects.all()
    search_fields = [
        "no__icontains",
        "name__icontains",
    ]


class JobFilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = {
            "no",
            "product",
            "customer",
            "route",
            "color_standard",
        }

    no = django_filters.CharFilter(
        field_name="no",
        lookup_expr="icontains",
        label="Job",
        widget=JobWidget(),
    )
    product = django_filters.CharFilter(
        label="Product",
        widget=ProductWidget(),
    )
    customer = django_filters.CharFilter(
        label="Customer",
        widget=CustomerWidget(),
    )
    route = django_filters.CharFilter(
        label="Route",
        widget=RouteWidget(),
    )
    color_standard = django_filters.CharFilter(
        label="Color Standard",
        widget=ColorStandardWidget(),
    )


class JobTestFilter(django_filters.FilterSet):
    class Meta:
        model = JobTest
        fields = (
            "job",
            "status",
            "current_machine",
            "raw_material",
            "route",
            "color_standard",
        )

    job = django_filters.CharFilter(
        field_name="job",
        lookup_expr="icontains",
        label="Job",
        widget=JobWidget(),
    )
    current_machine = django_filters.CharFilter(
        label="Current Machine",
        widget=MachineWidget(),
    )
    raw_material = django_filters.CharFilter(
        label="Raw Material",
        widget=RawMaterialWidget(),
    )
    route = django_filters.CharFilter(
        label="Route",
        widget=RouteWidget(),
    )
    color_standard = django_filters.CharFilter(
        label="Color Standard",
        widget=ColorStandardWidget(),
    )
