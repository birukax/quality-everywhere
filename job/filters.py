import django_filters
from .models import Job, JobTest
from main.custom_widgets import (
    JobWidget,
    CustomerWidget,
    ProductWidget,
    MachineWidget,
    RouteWidget,
    ColorStandardWidget,
    RawMaterialWidget,
)


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
            "status",
            "job",
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
    route = django_filters.CharFilter(
        label="Route",
        widget=RouteWidget(),
    )
    current_machine = django_filters.CharFilter(
        label="Current Machine",
        widget=MachineWidget(),
    )
    raw_material = django_filters.CharFilter(
        label="Raw Material",
        widget=RawMaterialWidget(),
    )
    color_standard = django_filters.CharFilter(
        label="Color Standard",
        widget=ColorStandardWidget(),
    )
