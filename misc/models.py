from django.db import models
from django.urls import reverse
from django.db.models.functions import Lower


class Customer(models.Model):
    no = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class ColorStandard(models.Model):
    name = models.CharField(max_length=100, unique=True)
    colors = models.ManyToManyField(
        "misc.Color",
        blank=True,
        related_name="color_standards",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"), name="unique_case_insensitive_color_standard_name"
            )
        ]
        ordering = ["name"]

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=100, unique=True)
    viscosity = models.FloatField(default=0)
    code = models.CharField(max_length=100, unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"), name="unique_case_insensitive_color_name"
            )
        ]
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}-{self.code}"


class RawMaterial(models.Model):
    name = models.CharField(max_length=100)
    thickness = models.IntegerField(null=True, blank=True)


    class Meta:
        # constraints = [
        #     models.UniqueConstraint(
        #         Lower("name"), name="unique_case_insensitive_RM_name"
        #     )
        # ]
        ordering = ["name",'thickness']

    def __str__(self):
        if self.thickness == None:
            return self.name
        else:
            return self.name + "-" + self.thickness


class Shift(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"), name="unique_case_insensitive_shift_name"
            )
        ]
        ordering = ["name"]

    def __str__(self):
        return self.name


# class Unit(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()

#     def __str__(self):
#         return self.name
