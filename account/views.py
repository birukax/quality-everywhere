from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from main.tasks import get_page, role_check
from .models import Profile
from .forms import CreateUserForm, EditUserForm, EditProfileForm, UpdateProfileForm


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


@login_required
@role_check(["ADMIN"])
def list(request):
    users = User.objects.exclude(id=request.user.id).order_by("username")
    page = get_page(request, model=users)
    context = {"page": page}
    return render(request, "registration/user/list.html", context)


@login_required
@role_check(["ADMIN"])
def detail(request, id):
    user = get_object_or_404(User, id=id)
    context = {"user": user}
    return render(request, "registration/user/detail.html", context)


@login_required
@role_check(["ADMIN"])
def create(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )
            user.save()
            user.set_password(form.cleaned_data["password"])
            user.save()
            Profile.objects.create(
                user=user,
                department=form.cleaned_data["department"],
                role=form.cleaned_data["role"],
            )
            return redirect("account:list")
    else:
        form = CreateUserForm()
    context = {"form": form}
    return render(request, "registration/user/create.html", context)


@login_required
@role_check(["ADMIN"])
def edit(request, id):
    user = get_object_or_404(User, id=id)
    if user == request.user:
        return redirect("account:list")
    if request.method == "POST":
        user_form = EditUserForm(request.POST, instance=user)
        profile_form = EditProfileForm(request.POST, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("account:list")
    else:
        user_form = EditUserForm(instance=user)
        profile_form = EditProfileForm(instance=user.profile)
    print(user.username)
    context = {"user": user, "user_form": user_form, "profile_form": profile_form}
    return render(request, "registration/user/edit.html", context)


@login_required
def profile(request):
    user = request.user
    form = UpdateProfileForm(instance=user)
    context = {"user": user, "form": form}
    return render(request, "registration/profile/detail.html", context)


@login_required
def update(request):
    user = request.user
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
    return redirect("account:profile")
