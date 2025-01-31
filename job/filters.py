import django_filters
from django_select2 import forms as s2forms

from .models import Job, JobTest


class JobWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "no__icontains",
    ]


class CustomerWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "no__icontains",
        "name__icontains",
    ]


class ProductWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "product__no__icontains",
        "product__name__icontains",
    ]


class MachineWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
    ]


class RouteWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
    ]


class ColorStandardWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
        "name__icontains",
    ]


class RawMaterialWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "no__icontains",
        "name__icontains",
    ]


class JobFilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = (
            "no",
            "product",
            "customer",
            "route",
            "color_standard",
        )
        widgets = {
            "no": JobWidget,
            "customer": CustomerWidget,
            "product": ProductWidget,
            "route": RouteWidget,
            "color_standard": ColorStandardWidget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["no"].label = "Job"
        self.filters["product"].label = "Product"
        self.filters["customer"].label = "Customer"
        self.filters["route"].label = "Route"
        self.filters["color_standard"].label = "Color Standard"


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
        widgets = {
            "job": JobWidget,
            "current_machine": MachineWidget,
            "raw_material": RawMaterialWidget,
            "route": RouteWidget,
            "color_standard": ColorStandardWidget,
        }
