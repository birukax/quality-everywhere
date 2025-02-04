import django_filters
from .models import Customer, Color, ColorStandard, RawMaterial, Shift
from main.custom_widgets import (
    CustomerWidget,
    ColorWidget,
    ColorStandardWidget,
    RawMaterialWidget,
    ShiftWidget,
)


class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = ["id"]

    id = django_filters.CharFilter(
        label="Customer",
        widget=CustomerWidget(),
    )


class ColorFilter(django_filters.FilterSet):
    class Meta:
        model = Color
        fields = ["id"]

    id = django_filters.CharFilter(
        label="Color",
        widget=ColorWidget(),
    )


class ColorStandardFilter(django_filters.FilterSet):
    class Meta:
        model = ColorStandard
        fields = ["id"]

    id = django_filters.CharFilter(
        label="Standard",
        widget=ColorStandardWidget(),
    )


class RawMaterialFilter(django_filters.FilterSet):
    class Meta:
        model = RawMaterial
        fields = ["id"]

    id = django_filters.CharFilter(
        label="Raw Material",
        widget=RawMaterialWidget(),
    )


class ShiftFilter(django_filters.FilterSet):
    class Meta:
        model = Shift
        fields = ["id"]

    id = django_filters.CharFilter(
        label="Shift",
        widget=ShiftWidget(),
    )
