from django.db import models
from django.db.models.functions import Lower

MACHINE_TYPE = (
    ("PRE-PRESS", "PRE-PRESS"),
    ("POST-PRESS", "POST-PRESS"),
    ("PRESS", "PRESS"),
    ("LAMINATION", "LAMINATION"),
    # ("BINDER", "BINDER"),
    ("PACKAGING", "PACKAGING"),
)


class Machine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=100, choices=MACHINE_TYPE, blank=True, null=True)
    viscosity_test = models.BooleanField(default=False)
    tests = models.ManyToManyField(
        "assessment.Test", related_name="machines", blank=True
    )
    conformities = models.ManyToManyField(
        "assessment.Conformity", related_name="machines", blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"), name="unique_case_insensitive_machine_name"
            )
        ]
        ordering = ["name"]

    def __str__(self):
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"), name="unique_case_insensitive_route_name"
            )
        ]
        ordering = ["name"]

    def __str__(self):
        return self.name


class MachineRoute(models.Model):
    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        null=True,
        related_name="machine_routes",
    )
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name="route_machines"
    )
    order = models.IntegerField()

    def __str__(self):
        if self.route and self.machine:
            return f"{self.route.name} - {self.machine.name} - {self.order}"
        
        return f"{self.order}"
        # return f"{self.route.name} - {self.machine.name}"

