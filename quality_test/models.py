from django.db import models


class FirstOffTest(models.Model):
    first_off = models.ForeignKey(
        "first_off.FirstOff",
        on_delete=models.CASCADE,
        related_name="first_off_tests",
    )
    test = models.ForeignKey(
        "misc.Test",
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
