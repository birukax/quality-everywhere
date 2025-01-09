from django.db import models


class Machine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tests = models.ManyToManyField(
        "assesment.Test", related_name="machines", blank=True
    )
    conformities = models.ManyToManyField(
        "assesment.Conformity", related_name="conformities", blank=True
    )

    def __str__(self):
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MachineRoute(models.Model):
    sequence = models.IntegerField()
    machine = models.ForeignKey(
        Machine, on_delete=models.CASCADE, related_name="machine_routes"
    )
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name="route_machines"
    )

    class Meta:
        unique_together = ("machine", "route")
