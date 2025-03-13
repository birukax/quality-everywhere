import django_filters
from .models import (
    Department,
    Location,
    Issue,
    IssueType,
    Employee,
    Incident,
    IncidentType,
)
from main.custom_widgets import (
    DepartmentWidget,
    IssueTypeWidget,
    LocationWidget,
    EmployeeWidget,
    IncidentWidget,
    IncidentTypeWidget,
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


class IncidentFilter(django_filters.FilterSet):
    class Meta:
        model = Incident
        fields = (
            "employee",
            "location",
        )

    employee = django_filters.ModelChoiceFilter(
        queryset=Employee.objects.all(),
        label="Employee",
        widget=EmployeeWidget(),
    )
    location = django_filters.ModelChoiceFilter(
        queryset=Location.objects.all(),
        label="Location",
        widget=LocationWidget(),
    )


class IncidentTypeFilter(django_filters.FilterSet):

    class Meta:
        model = IncidentType
        fields = ["id"]

    id = django_filters.CharFilter(
        lookup_expr="exact",
        label="Incident Type",
        widget=IncidentTypeWidget(),
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


class EmployeeFilter(django_filters.FilterSet):
    class Meta:
        model = Employee
        fields = ("id", "department", "status")

    id = django_filters.CharFilter(
        lookup_expr="exact",
        label="Employee",
        widget=EmployeeWidget(),
    )
    department = django_filters.ModelChoiceFilter(
        queryset=Department.objects.all(),
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
