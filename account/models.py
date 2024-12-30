from django.db import models
from django.contrib.auth.models import User as auth_user
from django.urls import reverse

ROLES = (
    ("USER", "USER"),
    ("ADMIN", "ADMIN"),
    ("MANAGER", "MANAGER"),
    ("OPERATOR", "OPERATOR"),
    ("INSPECTOR", "INSPECTOR"),
    ("SUPERVISOR", "SUPERVISOR"),
)

class Profile(models.Model):

    user = models.OneToOneField(auth_user, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLES, max_length=20, default="USER")
    machine = models.ForeignKey(
        "misc.Machine", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.user.username}"
