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
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Color(models.Model):
    color_standard = models.ForeignKey(
        "misc.ColorStandard", on_delete=models.CASCADE, related_name="colors"
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    no = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]


class Paper(models.Model):
    no = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Shift(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Test(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # type = models.CharField(max_length=100)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
