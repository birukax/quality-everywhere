from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Job, JobTest
from product.models import Artwork
from machine.models import Route, MachineRoute
from .tasks import job_get
from .forms import EditJobForm, CreateJobTestForm


@login_required
def list(request):
    jobs = Job.objects.all()
    context = {"jobs": jobs}
    return render(request, "job/list.html", context)


@login_required
def test_list(request):
    job_tests = JobTest.objects.all()
    context = {"job_tests": job_tests}
    return render(request, "job/test/list.html", context)


@login_required
def test_detail(request, id):
    context = {}
    first_off_ready = False
    on_process_ready = False
    next_machine = False
    job_test = get_object_or_404(JobTest, id=id)
    if job_test.status == "READY":
        first_off_ready = True
    if job_test.status == "FIRST-OFF COMPLETED":
        on_process_ready = True
    if job_test.status in ("ON-PROCESS CREATED"):
        next_machine = True
    context["job_test"] = job_test
    context["next_machine"] = next_machine
    context["first_off_ready"] = first_off_ready
    context["on_process_ready"] = on_process_ready
    return render(request, "job/test/detail.html", context)


@login_required
def next_machine(request, id):
    job_test = JobTest.objects.get(id=id)
    route = MachineRoute.objects.get(
        route=job_test.route, machine=job_test.current_machine
    )
    print(job_test.route, route.order)
    next_machine = MachineRoute.objects.filter(
        route=job_test.route, order=route.order + 1
    )
    if next_machine:
        job_test.current_machine = next_machine[0].machine
        job_test.status = "READY"
        job_test.save()
    else:
        job_test.current_machine = None
        job_test.status = "COMPLETED"
        job_test.save()
    return redirect("job:test_detail", id=job_test.id)


@login_required
def get_jobs(request):
    job_get()
    return redirect("job:list")


@login_required
def detail(request, id):
    context = {}
    ready = False

    job = get_object_or_404(Job, id=id)
    if Artwork.objects.filter(product=job.product):
        artwork = Artwork.objects.filter(product=job.product).latest("created_at")
        context["artwork"] = artwork
    edit_job_form = EditJobForm(instance=job)
    if JobTest.objects.filter(~Q(status="COMPLETED"), job=job).exists():
        unfinished_test = JobTest.objects.filter(
            ~Q(status="COMPLETED"), job=job
        ).first()
        context["unfinished_test"] = unfinished_test
    if job.route and job.product:
        ready = True
    context["job"] = job
    context["ready"] = ready
    context["edit_job_form"] = edit_job_form
    return render(request, "job/detail.html", context)


@login_required
def edit(request, id):
    job = get_object_or_404(Job, id=id)
    if request.method == "POST":
        form = EditJobForm(request.POST, instance=job)
        if form.is_valid():
            job.customer = form.cleaned_data["customer"]
            job.route = form.cleaned_data["route"]
            job.color_standard = form.cleaned_data["color_standard"]
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
                raw_material=form.cleaned_data["raw_material"],
                batch_no=form.cleaned_data["batch_no"],
                created_by=request.user,
            )
            if Artwork.objects.filter(product=job.product).exists():
                job_test.artwork = Artwork.objects.filter(product=job.product).latest(
                    "created_at"
                )
            job_test.save()
            return redirect("job:detail", id=id)
    else:
        form = CreateJobTestForm()
    context["form"] = form
    context["job"] = job
    return render(request, "job/test/create.html", context)
