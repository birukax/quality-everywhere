import django_filters
from .models import Machine, Route
from main.custom_widgets import MachineWidget, RouteWidget


class MachineFilter(django_filters.FilterSet):

    class Meta:
        model = Machine
        fields = (
            "name",
            "type",
            "viscosity_test",
        )

    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label="Machine Name",
        widget=MachineWidget(),
    )


class RouteFilter(django_filters.FilterSet):

    class Meta:
        model = Route
        fields = (
            "name",
            "active",
        )

    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label="Route Name",
        widget=RouteWidget(),
    )
