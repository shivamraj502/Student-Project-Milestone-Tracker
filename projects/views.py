from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group
import csv

from .models import Project, Guide, Milestone, Evaluation
from .forms import ProjectForm, GuideAllotmentForm, MilestoneForm, EvaluationForm


def get_role_name(role):
    return role.capitalize()


def user_has_role(user, role):
    return user.is_superuser or user.groups.filter(name=get_role_name(role)).exists()


def student_required(view_func):
    return user_passes_test(
        lambda u: u.is_superuser or u.groups.filter(name="Student").exists(),
        login_url="auth_selection",
    )(view_func)


def guide_required(view_func):
    return user_passes_test(
        lambda u: u.is_superuser or u.groups.filter(name="Guide").exists(),
        login_url="auth_selection",
    )(view_func)


def auth_selection(request):
    if request.user.is_authenticated:
        return redirect("home")

    return render(request, "auth_selection.html")


def role_login(request, role):
    role = role.lower()
    if role not in ["student", "guide"]:
        raise Http404()

    if request.user.is_authenticated:
        return redirect("home")

    login_form = AuthenticationForm(
        request=request, data=request.POST if "login_submit" in request.POST else None
    )
    signup_form = UserCreationForm(
        request.POST if "signup_submit" in request.POST else None
    )

    if request.method == "POST":
        if "login_submit" in request.POST and login_form.is_valid():
            user = login_form.get_user()
            if user_has_role(user, role):
                login(request, user)
                return redirect("home")
            login_form.add_error(
                None, f"This account is not registered as a {get_role_name(role)}."
            )
        elif "signup_submit" in request.POST and signup_form.is_valid():
            user = signup_form.save()
            group, _ = Group.objects.get_or_create(name=get_role_name(role))
            user.groups.add(group)
            user.save()

            if role == "guide":
                Guide.objects.create(user=user, name=user.username)

            login(request, user)
            return redirect("home")

    return render(
        request,
        "role_login.html",
        {
            "login_form": login_form,
            "signup_form": signup_form,
            "role": get_role_name(role),
        },
    )


@login_required(login_url="auth_selection")
def user_logout(request):
    logout(request)
    return redirect("auth_selection")


@login_required(login_url="auth_selection")
def home(request):
    context = {
        "project_count": Project.objects.count(),
        "milestone_count": Milestone.objects.count(),
        "guide_count": Guide.objects.count(),
        "evaluation_count": Evaluation.objects.count(),
    }
    return render(request, "home.html", context)


@login_required(login_url="auth_selection")
def project_list(request):
    if request.user.is_superuser:
        projects = Project.objects.all()
    elif user_has_role(request.user, "guide"):
        guide = Guide.objects.filter(user=request.user).first()
        projects = (
            Project.objects.filter(guide=guide) if guide else Project.objects.none()
        )
    else:
        projects = Project.objects.all()

    return render(request, "project_list.html", {"projects": projects})


@login_required(login_url="auth_selection")
@student_required
def register_project(request):
    form = ProjectForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("register")

    return render(request, "register.html", {"form": form})


@login_required(login_url="auth_selection")
def allot_guide(request, pk):
    project = Project.objects.get(id=pk)
    form = GuideAllotmentForm(request.POST or None, instance=project)

    if form.is_valid():
        form.save()
        return redirect("register")

    return render(request, "admin_allotment.html", {"form": form})


@login_required(login_url="auth_selection")
@student_required
def upload_milestone(request):
    form = MilestoneForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect("upload")

    return render(request, "upload.html", {"form": form})


@login_required(login_url="auth_selection")
@guide_required
def evaluate_project(request):
    form = EvaluationForm(request.POST or None, request.FILES or None)

    if request.user.is_superuser:
        project_queryset = Project.objects.all()
    else:
        guide = Guide.objects.filter(user=request.user).first()
        project_queryset = (
            Project.objects.filter(guide=guide) if guide else Project.objects.none()
        )

    form.fields["project"].queryset = project_queryset

    if form.is_valid():
        form.save()
        return redirect("evaluate")

    return render(request, "guide_evaluation.html", {"form": form})


@login_required(login_url="auth_selection")
def export_projects_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="projects_export.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ["Title", "Domain", "Team Members", "Marks", "Publication Status", "Guide"]
    )

    projects = Project.objects.all()

    domain = request.GET.get("domain")
    guide_id = request.GET.get("guide_id")
    publication_status = request.GET.get("publication")

    if domain:
        projects = projects.filter(domain__iexact=domain)
    if guide_id:
        projects = projects.filter(guide_id=guide_id)
    if publication_status:
        is_published = publication_status.lower() == "true"
        projects = projects.filter(evaluation__publication_status=is_published)

    for project in projects.distinct():
        team_members = filter(
            None,
            [
                project.student1_name,
                project.student2_name,
                project.student3_name,
                project.student4_name,
            ],
        )
        team_str = ", ".join(team_members)

        evaluations = project.evaluation_set.all()
        marks = evaluations.first().marks if evaluations.exists() else "N/A"
        pub_status = (
            "Yes"
            if (evaluations.exists() and evaluations.first().publication_status)
            else "No"
        )
        guide_name = project.guide.name if project.guide else "Unassigned"

        writer.writerow(
            [project.title, project.domain, team_str, marks, pub_status, guide_name]
        )

    return response
