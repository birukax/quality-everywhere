from django.db import models
import datetime
from django.contrib.auth.models import User
from django.urls import reverse
import django.utils.timezone
from main.validators import validate_ratio_format


class Assessment(models.Model):
    STATUS = (
        ("OPEN", "OPEN"),
        ("PENDING", "PENDING"),
        ("REJECTED", "REJECTED"),
        ("COMPLETED", "COMPLETED"),
    )
    TYPE = (
        ("FIRST-OFF", "FIRST-OFF"),
        ("ON-PROCESS", "ON-PROCESS"),
    )
    job_test = models.ForeignKey("job.JobTest", on_delete=models.RESTRICT)
    type = models.CharField(
        max_length=20,
        choices=TYPE,
        null=True,
        blank=True,
    )
    date = models.DateField(default=datetime.datetime.now)
    time = models.TimeField(default=datetime.datetime.now)
    route_no = models.PositiveIntegerField(default=1)
    extra = models.BooleanField(default=False)
    reason = models.TextField(max_length=200, null=True)
    shift = models.ForeignKey("misc.Shift", on_delete=models.RESTRICT)
    machine = models.ForeignKey(
        "machine.Machine", on_delete=models.CASCADE, null=True, blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="OPEN",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    inspected_by = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name="inspected_assessments",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        if self.type == "FIRST-OFF":
            return reverse("assessment:first_off_detail", args={self.id})
        elif self.type == "ON-PROCESS":
            return reverse("assessment:on_process_detail", args={self.id})

    def __str__(self):
        return f"{self.job_test.job} - {self.machine}"


class Test(models.Model):
    name = models.CharField(max_length=100, unique=True)
    critical = models.BooleanField(default=False)
    # type = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Conformity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # type = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "conformities"

    def __str__(self):
        return self.name


class Waste(models.Model):
    quantity = models.PositiveIntegerField()
    shift = models.ForeignKey(
        "misc.Shift",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    assessment = models.ForeignKey(
        "assessment.Assessment",
        on_delete=models.CASCADE,
        related_name="wastes",
    )
    machine = models.ForeignKey(
        "machine.Machine",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.shift.name} - {self.assessment}"


class SemiWaste(models.Model):
    job_test = models.ForeignKey(
        "job.JobTest", on_delete=models.RESTRICT, related_name="semi_wastes"
    )
    quantity = models.PositiveIntegerField()
    tag_no = models.CharField(max_length=30, unique=True)
    remark = models.TextField(max_length=200, null=True, blank=True)
    comment = models.TextField(max_length=200, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("OPEN", "OPEN"),
            ("COMPLETED", "COMPLETED"),
        ],
        default="OPEN",
    )
    approved_quantity = models.PositiveIntegerField(default=0)
    rejected_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name="created_semi_wastes",
        blank=True,
        null=True,
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name="approved_semi_wastes",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = "semi_wastes"

    def __str__(self):
        return f"{self.tag_no}"


class Viscosity(models.Model):
    reel_no = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )
    assessment = models.ForeignKey(
        "assessment.Assessment",
        on_delete=models.CASCADE,
        related_name="viscosities",
    )
    color = models.ForeignKey(
        "misc.Color",
        on_delete=models.CASCADE,
        related_name="viscosities",
    )
    value = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name="created_viscosities",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = "viscosities"


class Lamination(models.Model):
    ply_structure = models.PositiveIntegerField(default=2)
    assessment = models.OneToOneField(
        "assessment.Assessment",
        on_delete=models.CASCADE,
        related_name="lamination",
    )
    type = models.CharField(
        max_length=30,
        choices=[("SOLVENTLESS", "SOLVENTLESS"), ("SOLVENT-BASE", "SOLVENT-BASE")],
    )
    mixing_ratio = models.CharField(max_length=20, validators=[validate_ratio_format])
    adhesive = models.CharField(
        max_length=50,
    )
    adhesive_batch_no = models.CharField(
        max_length=30,
    )
    hardner = models.CharField(
        max_length=50,
    )
    hardner_batch_no = models.CharField(
        max_length=30,
    )
    supplier = models.CharField(
        max_length=50,
    )


class Substrate(models.Model):
    no = models.PositiveIntegerField(default=1)
    lamination = models.ForeignKey(
        Lamination,
        on_delete=models.RESTRICT,
        related_name="substrates",
    )
    raw_material = models.ForeignKey(
        "misc.RawMaterial",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    batch_no = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ("lamination", "raw_material")
        ordering = ["no"]


class FirstOff(models.Model):
    TYPE = (
        ("PASS", "PASS"),
        ("FAIL", "FAIL"),
        ("N/A", "N/A"),
    )
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="first_offs",
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
    )
    value = models.CharField(choices=TYPE, default="N/A", max_length=20)
    remark = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ["updated_at"]

    def __str__(self):
        return f"{self.assessment.machine} - {self.test}"


class OnProcess(models.Model):
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="on_processes",
    )
    conformity = models.ForeignKey(
        Conformity,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    sample_no = models.PositiveIntegerField(editable=False, default=1)
    shift = models.ForeignKey(
        "misc.Shift",
        on_delete=models.CASCADE,
    )
    action = models.TextField(
        max_length=300,
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name="created_on_processes",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        unique_together = ("assessment", "sample_no")

    def __str__(self):
        return f"{self.assessment.machine} - {self.conformity}"

    def save(self, *args, **kwargs):
        last_sample = (
            OnProcess.objects.filter(assessment=self.assessment)
            .order_by("-sample_no")
            .first()
        )
        if last_sample:
            self.sample_no = last_sample.sample_no + 1
        else:
            self.sample_no = 1

        super().save(*args, **kwargs)
