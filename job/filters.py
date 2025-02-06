import django_filters
from .models import Job, JobTest
from main.custom_widgets import (
    JobWidget,
    JobTestWidget,
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
            "id",
            "product",
            "customer",
            "route",
            "color_standard",
        )

    id = django_filters.CharFilter(
        lookup_expr="exact",
        label="Job",
        widget=JobWidget(),
    )
    product = django_filters.CharFilter(
        label="Product",
        lookup_expr="exact",
        widget=ProductWidget(),
    )
    customer = django_filters.CharFilter(
        label="Customer",
        lookup_expr="exact",
        widget=CustomerWidget(),
    )
    route = django_filters.CharFilter(
        label="Route",
        lookup_expr="exact",
        widget=RouteWidget(),
    )
    color_standard = django_filters.CharFilter(
        label="Color Standard",
        lookup_expr="exact",
        widget=ColorStandardWidget(),
    )


class JobTestFilter(django_filters.FilterSet):
    class Meta:
        model = JobTest
        fields = (
            "id",
            "job",
            "status",
            "current_machine",
            "raw_material",
            "route",
            "color_standard",
        )

    id = django_filters.CharFilter(
        lookup_expr="exact",
        label="Test",
        widget=JobTestWidget(),
    )
    job = django_filters.CharFilter(
        field_name="job",
        lookup_expr="exact",
        label="Job",
        widget=JobWidget(),
    )
    route = django_filters.CharFilter(
        label="Route",
        lookup_expr="exact",
        widget=RouteWidget(),
    )
    current_machine = django_filters.CharFilter(
        label="Current Machine",
        lookup_expr="exact",
        widget=MachineWidget(),
    )
    raw_material = django_filters.CharFilter(
        label="Raw Material",
        lookup_expr="exact",
        widget=RawMaterialWidget(),
    )
    color_standard = django_filters.CharFilter(
        label="Color Standard",
        lookup_expr="exact",
        widget=ColorStandardWidget(),
    )
