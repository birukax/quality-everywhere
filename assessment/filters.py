import django_filters
from django_select2 import forms as s2forms
from .models import Assessment, Waste, SemiWaste, Test, Conformity
from django import forms
from main.custom_widgets import (
    JobTestWidget,
    MachineWidget,
    UserWidget,
    ShiftWidget,
    SemiWasteWidget,
    TestWidget,
    ConformityWidget,
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
        widget=django_filters.widgets.DateRangeWidget(attrs={"type": "date"}),
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


class SemiWasteFilter(django_filters.FilterSet):
    class Meta:
        model = SemiWaste
        fields = (
            "id",
            "job_test",
            "status",
        )

    id = django_filters.CharFilter(
        label="Tag No.",
        lookup_expr="exact",
        widget=SemiWasteWidget(),
    )
    job_test = django_filters.CharFilter(
        label="Job Test",
        lookup_expr="exact",
        widget=JobTestWidget(),
    )


class WasteFilter(django_filters.FilterSet):
    class Meta:
        model = Waste
        fields = (
            "assessment__job_test",
            "machine",
            "shift",
        )

    assessment__job_test = django_filters.CharFilter(
        label="Job Test",
        lookup_expr="exact",
        widget=JobTestWidget(),
    )
    machine = django_filters.CharFilter(
        label="Machine",
        lookup_expr="exact",
        widget=MachineWidget(),
    )
    shift = django_filters.CharFilter(
        label="Shift",
        lookup_expr="exact",
        widget=ShiftWidget(),
    )


class TestFilter(django_filters.FilterSet):
    class Meta:
        model = Test
        fields = ("id", "critical")

    id = django_filters.CharFilter(
        label="Test Name",
        lookup_expr="exact",
        widget=TestWidget(),
    )
    critical = django_filters.BooleanFilter(
        label="Critial",
        lookup_expr="exact",
        widget=forms.Select(
            attrs={
                "class": "w-full items-center text-center h-auto",
            },
            choices=(
                ("", "---------"),
                (True, "Yes"),
                (False, "No"),
            ),
        ),
    )


class ConformityFilter(django_filters.FilterSet):
    class Meta:
        model = Conformity
        fields = ["id"]

    id = django_filters.CharFilter(
        label="Conformity",
        lookup_expr="exact",
        widget=ConformityWidget(),
    )
