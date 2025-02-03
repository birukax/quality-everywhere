import django_filters
from .models import AssessmentApproval
from main.custom_widgets import JobTestWidget, MachineWidget, UserWidget, ShiftWidget


class AssessmentApprovalFilter(django_filters.FilterSet):
    class Meta:
        model = AssessmentApproval
        fields = ("assessment__job_test",)

    assessment__job_test = django_filters.CharFilter(
        field_name="assessment__job_test",
        lookup_expr="exact",
        label="Job Test",
        widget=JobTestWidget(),
    )
    assessment__machine = django_filters.CharFilter(
        field_name="assessment__machine",
        lookup_expr="exact",
        label="Machine",
        widget=MachineWidget(),
    )
    assessment__shift = django_filters.CharFilter(
        field_name="assessment__shift",
        lookup_expr="exact",
        label="Shift",
        widget=ShiftWidget(),
    )
    assessment__inspected_by = django_filters.CharFilter(
        field_name="assessment__inspected_by",
        lookup_expr="exact",
        label="Inspected By",
        widget=UserWidget(),
    )
