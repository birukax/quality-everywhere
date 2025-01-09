from django.db import models

MACHINE_TYPE = (
    ("PRE-PRESS", "PRE-PRESS"),
    ("POST-PRESS", "POST-PRESS"),
    ("PRESS", "PRESS"),
    ("LAMINATION", "LAMINATION"),
    ("BINDER", "BINDER"),
    ("PACKAGING", "PACKAGING"),
)


class Machine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=100, choices=MACHINE_TYPE, blank=True, null=True)
    tests = models.ManyToManyField(
        "assesment.Test", related_name="machines", blank=True
    )
    conformities = models.ManyToManyField(
        "assesment.Conformity", related_name="conformities", blank=True
    )

    def __str__(self):
        return self.name


class Route(models.Model):
    order = models.IntegerField(null=True)
    name = models.CharField(max_length=100, unique=True)
    machine = models.ForeignKey(
        Machine, on_delete=models.CASCADE, related_name="machine_routes"
    )

    class Meta:
        unique_together = ("name", "order")

    def __str__(self):
        return self.name
