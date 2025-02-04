import django_filters
from .models import Machine, Route
from main.custom_widgets import MachineWidget, RouteWidget


class MachineFilter(django_filters.FilterSet):

    class Meta:
        model = Machine
        fields = (
            "id",
            "type",
            "viscosity_test",
        )

    id = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Machine Name",
        widget=MachineWidget(),
    )


class RouteFilter(django_filters.FilterSet):

    class Meta:
        model = Route
        fields = (
            "id",
            "active",
        )

    id = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Route Name",
        widget=RouteWidget(),
    )
