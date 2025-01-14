from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job, JobTest
from machine.models import Route, MachineRoute
from .tasks import job_get
from .forms import EditJobForm, CreateJobTestForm


@login_required
def list(request):
    jobs = Job.objects.all()
    return render(request, "job/list.html", {"jobs": jobs})


@login_required
def test_list(request):
    job_tests = JobTest.objects.all()
    return render(request, "job/test/list.html", {"job_tests": job_tests})


@login_required
def test_detail(request, id):
    job_test = get_object_or_404(JobTest, id=id)
    return render(request, "job/test/detail.html", {"job_test": job_test})


@login_required
def get_jobs(request):
    job_get()
    return redirect("job:list")


@login_required
def detail(request, id):
    ready = False
    job = get_object_or_404(Job, id=id)
    edit_job_form = EditJobForm(instance=job)
    unfinished_tests = job.job_tests.all().exclude(status="COMPLETED")
    if job.artwork and job.route and job.press_machine and job.product:
        ready = True
    context = {
        "job": job,
        "ready": ready,
        "edit_job_form": edit_job_form,
        "unfinished_tests": unfinished_tests,
    }
    return render(request, "job/detail.html", context)


@login_required
def edit(request, id):
    job = get_object_or_404(Job, id=id)
    if request.method == "POST":
        form = EditJobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            job.customer = form.cleaned_data["customer"]
            job.route = form.cleaned_data["route"]
            job.press_machine = form.cleaned_data["press_machine"]
            job.color_standard = form.cleaned_data["color_standard"]
            job.certificate_no = form.cleaned_data["certificate_no"]
            job.artwork_approved = form.cleaned_data["artwork_approved"]
            job.artwork = form.cleaned_data["artwork"]
            job.save()
        else:
            print(form.errors)
    return redirect("job:detail", id=id)


@login_required
def create_test(request, id):
    context = {}
    job = get_object_or_404(Job, id=id)
    if request.method == "POST":
        form = CreateJobTestForm(request.POST)
        if form.is_valid():
            route = Route.objects.get(id=job.route.id)
            current_machine = MachineRoute.objects.get(route=route, order=1)
            job_test = JobTest(
                job=job,
                route=job.route,
                color_standard=job.color_standard,
                current_machine=current_machine.machine,
                paper=form.cleaned_data["paper"],
                batch_no=form.cleaned_data["batch_no"],
                created_by=request.user,
            )
            job_test.save()
            return redirect("job:detail", id=id)
    else:
        form = CreateJobTestForm()
    context["form"] = form
    context["job"] = job
    return render(request, "job/test/create.html", context)
