import django_filters
from django_select2 import forms as s2forms
from .models import Assessment, SemiWaste, Test, Conformity
from django import forms
from main.custom_widgets import (
    JobWidget,
    JobTestWidget,
    CustomerWidget,
    ProductWidget,
    MachineWidget,
    RouteWidget,
    ColorStandardWidget,
    RawMaterialWidget,
    UserWidget,
    ShiftWidget,
)


class AssessmentFilter(django_filters.FilterSet):
    class Meta:
        model = Assessment
        fields = (
            "job_test",
            "shift",
            "machine",
            "status",
            "inspected_by",
            "date",
        )

    job_test = django_filters.CharFilter(
        label="Job Test",
        lookup_expr="exact",
        widget=JobTestWidget(),
    )
    date = django_filters.DateFromToRangeFilter(
        label="Date Range",
        widget=django_filters.widgets.DateRangeWidget(
            attrs={
                "type": "date",
                "placeholder": "YYYY/MM/DD",
            }
        ),
    )
    shift = django_filters.CharFilter(
        label="Shift",
        lookup_expr="exact",
        widget=ShiftWidget(),
    )
    machine = django_filters.CharFilter(
        label="Machine",
        lookup_expr="exact",
        widget=MachineWidget(),
    )
    inspected_by = django_filters.CharFilter(
        label="Inspected By",
        lookup_expr="exact",
        widget=UserWidget(),
    )
