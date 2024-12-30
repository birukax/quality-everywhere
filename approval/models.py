from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class FirstOffApproval(models.Model):
    first_off = models.ForeignKey("first_off.FirstOff", on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-approved_at"]
