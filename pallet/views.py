from django.shortcuts import render

# from .models import PalletCard, PalletMachine
from django.contrib.auth.decorators import login_required


@login_required
def list(request):
    pass
    # pallets = PalletCard.objects.all()
    # return render(request, "pallet/list.html", {"pallets": pallets})
