import csv

from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    EvaluationForm,
    GuideAllotmentForm,
    MilestoneForm,
    ProjectForm,
    RoleAuthenticationForm,
    RoleSignUpForm,
)
from .models import Evaluation, Guide, Milestone, Project
from .permissions import (
    ROLE_GUIDE,
    ROLE_STUDENT,
    admin_required,
    get_user_role,
    is_admin,
    is_guide,
    is_student,
    role_required,
)


def get_visible_projects(user):
    projects = Project.objects.select_related("guide", "created_by").prefetch_related(
        "milestone_set", "evaluation_set"
    ).order_by("title")
    if is_admin(user):
        return projects
    if is_student(user):
        return projects.filter(created_by=user)
    if is_guide(user):
        guide_profile = getattr(user, "guide_profile", None)
        return projects.filter(guide=guide_profile) if guide_profile else projects.none()
    return projects.none()


@role_required(ROLE_STUDENT, ROLE_GUIDE)
def home(request):
    visible_projects = get_visible_projects(request.user)
    visible_evaluations = Evaluation.objects.filter(project__in=visible_projects)
    visible_milestones = Milestone.objects.filter(project__in=visible_projects)

    if is_admin(request.user):
        guide_count = Guide.objects.count()
    elif is_guide(request.user):
        guide_count = 1 if getattr(request.user, "guide_profile", None) else 0
    else:
        guide_count = visible_projects.exclude(guide__isnull=True).values("guide").distinct().count()

    context = {
        "project_count": visible_projects.count(),
        "milestone_count": visible_milestones.count(),
        "guide_count": guide_count,
        "evaluation_count": visible_evaluations.count(),
    }
    return render(request, "home.html", context)


def auth_selection(request):
    if request.user.is_authenticated:
        if get_user_role(request.user) is None:
            logout(request)
        else:
            return redirect("home")
    return render(request, "auth_selection.html")


def role_auth(request, role):
    role_key = role.lower()
    role_map = {"student": ROLE_STUDENT, "guide": ROLE_GUIDE}
    if role_key not in role_map:
        raise Http404("Role not found.")

    if request.user.is_authenticated:
        if get_user_role(request.user):
            return redirect("home")
        logout(request)

    selected_role = role_map[role_key]
    login_form = RoleAuthenticationForm(request=request, prefix="login")
    signup_form = RoleSignUpForm(role=selected_role, prefix="signup")

    if request.method == "POST":
        action = request.POST.get("auth_action")
        if action == "login":
            login_form = RoleAuthenticationForm(request=request, data=request.POST, prefix="login")
            signup_form = RoleSignUpForm(role=selected_role, prefix="signup")
            if login_form.is_valid():
                user = login_form.get_user()
                user_role = get_user_role(user)
                if user_role == selected_role:
                    login(request, user)
                    messages.success(request, f"Signed in as {selected_role.lower()}.")
                    return redirect("home")
                if is_admin(user):
                    messages.error(request, "Admin accounts should use the /admin/ portal.")
                else:
                    messages.error(
                        request,
                        f"This account is not registered as a {selected_role.lower()}.",
                    )
        elif action == "signup":
            signup_form = RoleSignUpForm(request.POST, role=selected_role, prefix="signup")
            login_form = RoleAuthenticationForm(request=request, prefix="login")
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                messages.success(request, f"{selected_role} account created successfully.")
                return redirect("home")

    context = {
        "selected_role": selected_role,
        "login_form": login_form,
        "signup_form": signup_form,
    }
    return render(request, "role_auth.html", context)


def logout_view(request):
    logout(request)
    return redirect("auth_selection")


@role_required(ROLE_STUDENT, ROLE_GUIDE)
def project_list(request):
    projects = get_visible_projects(request.user)
    return render(request, "project_list.html", {"projects": projects})


@role_required(ROLE_STUDENT)
def register_project(request):
    form = ProjectForm(request.POST or None)

    if form.is_valid():
        project = form.save(commit=False)
        project.created_by = request.user
        project.save()
        messages.success(request, "Project registered successfully.")
        return redirect("register")

    return render(request, "register.html", {"form": form})


@admin_required
def allot_guide(request, pk):
    project = get_object_or_404(Project, id=pk)
    form = GuideAllotmentForm(request.POST or None, instance=project)

    if form.is_valid():
        form.save()
        messages.success(request, "Guide assigned successfully.")
        return redirect("projects_list")

    return render(request, "admin_allotment.html", {"form": form, "project": project})


@role_required(ROLE_STUDENT)
def upload_milestone(request):
    form = MilestoneForm(request.POST or None, request.FILES or None, user=request.user)

    if form.is_valid():
        milestone = form.save(commit=False)
        milestone.uploaded_by = request.user
        milestone.save()
        messages.success(request, "Milestone uploaded successfully.")
        return redirect("upload")

    return render(request, "upload.html", {"form": form})


@role_required(ROLE_GUIDE)
def evaluate_project(request):
    existing_evaluation = None
    selected_project_id = request.POST.get("project") if request.method == "POST" else None

    if selected_project_id:
        allowed_projects = get_visible_projects(request.user)
        selected_project = allowed_projects.filter(id=selected_project_id).first()
        if selected_project:
            existing_evaluation = Evaluation.objects.filter(project=selected_project).first()

    form = EvaluationForm(
        request.POST or None,
        request.FILES or None,
        user=request.user,
        instance=existing_evaluation,
    )

    if form.is_valid():
        evaluation = form.save(commit=False)
        evaluation.evaluated_by = request.user
        evaluation.save()
        messages.success(request, "Evaluation submitted successfully.")
        return redirect("evaluate")

    return render(request, "guide_evaluation.html", {"form": form})


@admin_required
def export_projects_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="projects_export.csv"'

    writer = csv.writer(response)
    writer.writerow(["Title", "Domain", "Team Members", "Marks", "Publication Status", "Guide"])

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
        pub_status = "Yes" if evaluations.exists() and evaluations.first().publication_status else "No"
        guide_name = project.guide.name if project.guide else "Unassigned"

        writer.writerow([project.title, project.domain, team_str, marks, pub_status, guide_name])

    return response
