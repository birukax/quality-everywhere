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


class FirstOff(models.Model):
    quality_test = models.ForeignKey(
        "quality_test.QualityTest",
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
        return f"{self.quality_test.machine} - {self.test}"


class OnProcess(models.Model):
    quality_test = models.ForeignKey(
        "quality_test.QualityTest",
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
        return f"{self.quality_test.machine} - {self.conformity}"
