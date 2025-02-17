import django_filters
from .models import Department, Location, Issue, IssueType
from main.custom_widgets import (
    DepartmentWidget,
    IssueTypeWidget,
    LocationWidget,
)


class IssueFilter(django_filters.FilterSet):

    class Meta:
        model = Issue
        fields = (
            "location",
            "department",
            "issue_type",
            "status",
            "type",
        )

    location = django_filters.ModelChoiceFilter(
        queryset=Location.objects.filter(active=True),
        label="Location",
        widget=LocationWidget(),
    )
    department = django_filters.ModelChoiceFilter(
        queryset=Department.objects.filter(active=True),
        label="Department",
        widget=DepartmentWidget(),
    )
    issue_type = django_filters.ModelChoiceFilter(
        queryset=IssueType.objects.filter(active=True),
        label="Issue Type",
        widget=IssueTypeWidget(),
    )


class DepartmentFilter(django_filters.FilterSet):

    class Meta:
        model = Department
        fields = ["id"]

    id = django_filters.CharFilter(
        lookup_expr="exact",
        label="Department",
        widget=DepartmentWidget(),
    )


class LocationFilter(django_filters.FilterSet):

    class Meta:
        model = Location
        fields = ["id"]

    id = django_filters.CharFilter(
        lookup_expr="exact",
        label="Location",
        widget=LocationWidget(),
    )


class IssueTypeFilter(django_filters.FilterSet):

    class Meta:
        model = IssueType
        fields = ["id"]

    id = django_filters.CharFilter(
        lookup_expr="exact",
        label="Issue Type",
        widget=IssueTypeWidget(),
    )
