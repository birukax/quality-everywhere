from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job
from first_off.models import FirstOff
from quality_test.models import FirstOffTest
from misc.models import Test, Machine
from .tasks import get_job
from .forms import EditJobForm, CreateFirstOffForm


@login_required
def list(request):
    get_job()
    jobs = Job.objects.all()
    return render(request, "job/list.html", {"jobs": jobs})


@login_required
def detail(request, id):
    job = get_object_or_404(Job, id=id)
    edit_job_form = EditJobForm(instance=job)
    create_first_off_form = CreateFirstOffForm()
    context = {
        "job": job,
        "edit_job_form": edit_job_form,
        "create_first_off_form": create_first_off_form,
    }
    return render(request, "job/detail.html", context)


@login_required
def edit(request, id):
    job = get_object_or_404(Job, id=id)
    if request.method == "POST":
        form = EditJobForm(request.POST, instance=job)
        if form.is_valid():
            job.customer = form.cleaned_data["customer"]
            job.machine = form.cleaned_data["machine"]
            job.color_standard = form.cleaned_data["color_standard"]
            job.certificate_no = form.cleaned_data["certificate_no"]
            job.save()
    return redirect("job:detail", id=id)


@login_required
def create_first_off(request, id):
    job = get_object_or_404(Job, id=id)
    if request.method == "POST":
        form = CreateFirstOffForm(request.POST)
        if form.is_valid():
            machines = form.cleaned_data["machines"]
            for machine in machines:
                first_off = FirstOff(
                    job=job,
                    machine=machine,
                    no=job.tests,
                )
                first_off.save()
                for t in machine.tests.all():
                    test = FirstOffTest(
                        first_off=first_off,
                        test=t,
                    )
                    test.save()
            job.tests = job.tests + 1
    return redirect("job:detail", id=id)
