import django
from django.db import models
from datetime import date, time, datetime

import django.utils
import django.utils.timezone


class Test(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # type = models.CharField(max_length=100)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Conformity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # type = models.CharField(max_length=100)

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "conformities"

    def __str__(self):
        return self.name


class FirstOffTest(models.Model):
    first_off = models.ForeignKey(
        "first_off.FirstOff",
        on_delete=models.CASCADE,
        related_name="first_off_tests",
    )
    test = models.ForeignKey(
        "assesment.Test",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    value = models.BooleanField(null=True, blank=True)
    remark = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.first_off.machine} - {self.test}"


class OnProcessConformity(models.Model):
    first_off = models.ForeignKey(
        "first_off.FirstOff",
        on_delete=models.CASCADE,
        related_name="on_process_conformities",
    )
    conformity = models.ForeignKey(
        "assesment.Conformity",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date = models.DateField(default=django.utils.timezone.now)
    time = models.TimeField(default=django.utils.timezone.now)
    action = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.first_off.machine} - {self.conformity}"
