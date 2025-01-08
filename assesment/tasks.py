from django.shortcuts import get_object_or_404
from .models import Test
from .forms import CreateTestForm, EditTestForm


def test_create(request):
    if request.method == "POST":
        form = CreateTestForm(request.POST)
        if form.is_valid():
            form.save()


def test_edit(request, id):
    test = get_object_or_404(Test, id=id)
    if request.method == "POST":
        form = EditTestForm(request.POST, instance=test)
        if form.is_valid():
            test.name = form.cleaned_data["name"]
            test.save()
