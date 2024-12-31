from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class FirstOff(models.Model):
    STATUS = (
        ("OPEN", "OPEN"),
        ("PENDING", "PENDING"),
        ("REJECTED", "REJECTED"),
        ("COMPLETED", "COMPLETED"),
    )
    job = models.ForeignKey("job.Job", on_delete=models.CASCADE)
    no = models.IntegerField(default=1)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    shift = models.ForeignKey(
        "misc.Shift",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    machine = models.ForeignKey("misc.Machine", on_delete=models.CASCADE)
    paper = models.ForeignKey(
        "misc.Paper",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    batch_no = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="OPEN",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_first_offs',
        blank=True,
        null=True,
    )
    inspected_by = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name='inspected_first_offs',
        blank=True,
        null=True,
        
    )
    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("first_off:detail", args={self.id})
