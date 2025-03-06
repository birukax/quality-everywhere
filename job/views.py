from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from .models import Job, JobTest
from product.models import Artwork
from machine.models import Route, MachineRoute
from assessment.models import SemiWaste, Assessment, OnProcess
from .tasks import job_get
from main.tasks import get_page, role_check
from .forms import EditJobForm, CreateJobTestForm
from .filters import JobFilter, JobTestFilter
from assessment.forms import CreateSemiWasteForm


@login_required
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
def list(request):
    jobs = Job.objects.select_related(
        "product", "customer", "route", "color_standard"
    ).all()
    job_filter = JobFilter(request.GET, queryset=jobs)
    jobs = job_filter.qs
    page = get_page(request, model=jobs)

    context = {
        "page": page,
        "filter": job_filter,
    }
    return render(request, "job/list.html", context)


@login_required
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
def get_jobs(request):
    job_get()
    return redirect("job:list")


@login_required
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
def detail(request, id):
    context = {}
    ready = False

    job = get_object_or_404(Job, id=id)
    if Artwork.objects.filter(product=job.product):
        artwork = Artwork.objects.filter(product=job.product).latest("created_at")
        context["artwork"] = artwork
    edit_job_form = EditJobForm(instance=job)
    if JobTest.objects.filter(
        ~Q(status__in=["COMPLETED", "FINISHED"]), job=job
    ).exists():
        unfinished_test = JobTest.objects.filter(
            ~Q(status__in=["COMPLETED", "FINISHED"]), job=job
        ).first()
        context["unfinished_test"] = unfinished_test
    if job.route and job.product:
        ready = True
    context["job"] = job
    context["ready"] = ready
    context["edit_job_form"] = edit_job_form
    return render(request, "job/detail.html", context)


@login_required
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
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
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
def test_list(request):
    job_tests = JobTest.objects.select_related("job", "route", "current_machine").all()
    job_test_filter = JobTestFilter(request.GET, queryset=job_tests)
    job_tests = job_test_filter.qs
    page = get_page(request, model=job_tests)

    context = {
        "page": page,
        "filter": job_test_filter,
    }
    return render(request, "job/test/list.html", context)


@login_required
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
def test_detail(request, id):
    context = {}
    first_off_ready = False
    on_process_ready = False
    next_machine = False
    ready_to_finish = False
    job_test = get_object_or_404(JobTest, id=id)
    create_semi_waste_form = CreateSemiWasteForm()
    semi_wastes = SemiWaste.objects.filter(job_test=job_test)
    empty_on_processes = Assessment.objects.annotate(on_processes_count=Count('on_processes')).filter(
            job_test=job_test, type='ON-PROCESS', on_processes_count=0
        )
    open_first_offs = Assessment.objects.filter(job_test=job_test, type='FIRST-OFF').exclude(status='COMPLETED')
    if job_test.status == "READY":
        first_off_ready = True
    if job_test.status == "FIRST-OFF COMPLETED":
        on_process_ready = True
    if job_test.status in ("ON-PROCESS CREATED"):
        next_machine = True
    open_semi_wastes = SemiWaste.objects.filter(job_test=job_test, status="OPEN")
    if (
        job_test.status == "COMPLETED"
        and not open_semi_wastes.exists()
        and job_test.current_machine == None
    and empty_on_processes.exists() == False
    and open_first_offs.exists() == False
    ):
        ready_to_finish = True
    context["job_test"] = job_test
    context["next_machine"] = next_machine
    context["first_off_ready"] = first_off_ready
    context["on_process_ready"] = on_process_ready
    context["ready_to_finish"] = ready_to_finish
    context["semi_wastes"] = semi_wastes
    context["form"] = create_semi_waste_form
    return render(request, "job/test/detail.html", context)


@login_required
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
def create_semi_waste(request, id):
    job_test = JobTest.objects.get(id=id)
    if request.method == "POST":
        form = CreateSemiWasteForm(request.POST)
        if form.is_valid():
            semi_waste = SemiWaste(
                job_test=job_test,
                quantity=form.cleaned_data["quantity"],
                tag_no=form.cleaned_data["tag_no"],
                remark=form.cleaned_data["remark"],
                created_by=request.user,
            )
            semi_waste.save()
    return redirect("job:test_detail", id=job_test.id)


@login_required
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
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
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
def finish_test(request, id):
    if request.method == "POST":
        job_test = JobTest.objects.get(id=id)
        open_semi_wastes = SemiWaste.objects.filter(job_test=job_test, status="OPEN")
        empty_on_processes = Assessment.objects.filter(
            job_test=job_test, type='ON-PROCESS', on_processes__isnull=True
        )
        if (
            job_test.status == "COMPLETED"
            and not open_semi_wastes.exists()
            and job_test.current_machine == None
        ) and not empty_on_processes.exists():
            on_processes = Assessment.objects.filter(
                job_test=job_test, type="ON-PROCESS"
            )
            for op in on_processes:
                op.status = "COMPLETED"
                op.save()

            job_test.status = "FINISHED"
            job_test.save()
    return redirect("job:test_detail", id=job_test.id)


@login_required
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
def create_test(request, id):
    context = {}
    job = get_object_or_404(Job, id=id)
    if request.method == "POST":
        form = CreateJobTestForm(request.POST)
        if form.is_valid():
            route = Route.objects.get(id=job.route.id)
            current_machine = MachineRoute.objects.get(route=route, order=1)
            job_test = JobTest(
                no=job.test_count,
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
            job.test_count = job.test_count + 1
            job.save()
            return redirect("job:detail", id=id)
    else:
        form = CreateJobTestForm()
    context["form"] = form
    context["job"] = job
    return render(request, "job/test/create.html", context)
