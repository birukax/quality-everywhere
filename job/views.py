from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job
from .tasks import job_get, create_first_offs
from .forms import EditJobForm, CreateFirstOffForm


@login_required
def list(request):
    job_get()
    jobs = Job.objects.all()
    return render(request, "job/list.html", {"jobs": jobs})


@login_required
def get_jobs(request):
    job_get()
    return redirect("job:list")


@login_required
def detail(request, id):
    job = get_object_or_404(Job, id=id)
    edit_job_form = EditJobForm(instance=job)
    create_first_off_form = CreateFirstOffForm()
    unfinished_first_offs = job.first_offs.all().exclude(status="COMPLETED")
    context = {
        "job": job,
        "edit_job_form": edit_job_form,
        "create_first_off_form": create_first_off_form,
        "unfinished_first_offs": unfinished_first_offs,
    }
    return render(request, "job/detail.html", context)


@login_required
def edit(request, id):
    job = get_object_or_404(Job, id=id)
    if request.method == "POST":
        form = EditJobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            job.customer = form.cleaned_data["customer"]
            job.machine = form.cleaned_data["machine"]
            job.color_standard = form.cleaned_data["color_standard"]
            job.certificate_no = form.cleaned_data["certificate_no"]
            job.artwork = form.cleaned_data["artwork"]
            job.save()
        else:
            print(form.errors)
    return redirect("job:detail", id=id)


@login_required
def create_first_off(request, id):
    create_first_offs(request, id)
    return redirect("job:detail", id=id)
