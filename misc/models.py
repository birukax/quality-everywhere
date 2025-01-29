from django.db import models
from django.urls import reverse


class Customer(models.Model):
    no = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]


class ColorStandard(models.Model):
    name = models.CharField(max_length=100, unique=True)
    colors = models.ManyToManyField(
        "misc.Color",
        blank=True,
        related_name="color_standards",
    )

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=100)
    viscosity = models.FloatField(default=0)
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}-{self.code}"


class RawMaterial(models.Model):
    no = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Shift(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# class Unit(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()

#     def __str__(self):
#         return self.name
