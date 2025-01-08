# from django.db import models
# from django.contrib.auth.models import User as auth_user


# class PalletCard(models.Model):
#     no = models.AutoField(primary_key=True)
#     job_description = models.CharField(max_length=50)
#     customer = models.ForeignKey(
#         "misc.Customer", on_delete=models.CASCADE, related_name="pallets"
#     )
#     reel_no = models.CharField(max_length=50)
#     inspected_by = models.ForeignKey(
#         auth_user, on_delete=models.CASCADE, related_name="pallets"
#     )
#     passed = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(
#         auth_user, on_delete=models.CASCADE, related_name="pallets_created"
#     )


# class PalletMachine(models.Model):
#     machine = models.ForeignKey("machine.Machine", on_delete=models.CASCADE)
#     date = models.DateField()
#     pallet = models.ForeignKey("pallet.PalletCard", on_delete=models.CASCADE)
#     shift = models.ForeignKey(
#         "misc.Shift", on_delete=models.CASCADE, null=True, blank=True
#     )
#     operator = models.ForeignKey(
#         auth_user, on_delete=models.CASCADE, null=True, blank=True
#     )
#     quantity = models.FloatField(null=True, blank=True)
#     unit = models.ForeignKey(
#         "misc.Unit", on_delete=models.CASCADE, null=True, blank=True
#     )
#     trim_size = models.CharField(max_length=50, null=True, blank=True)
#     comment = models.TextField()
