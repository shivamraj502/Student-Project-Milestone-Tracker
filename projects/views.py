from django.shortcuts import render, redirect
from .models import Project, Guide, Milestone, Evaluation
from .forms import ProjectForm, GuideAllotmentForm, MilestoneForm, EvaluationForm


def home(request):
    context = {
        "project_count": Project.objects.count(),
        "milestone_count": Milestone.objects.count(),
        "guide_count": Guide.objects.count(),
        "evaluation_count": Evaluation.objects.count(),
    }
    return render(request, "home.html", context)


def project_list(request):
    projects = Project.objects.all()
    return render(request, "project_list.html", {"projects": projects})


def register_project(request):
    form = ProjectForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("register")

    return render(request, "register.html", {"form": form})


def allot_guide(request, pk):
    project = Project.objects.get(id=pk)
    form = GuideAllotmentForm(request.POST or None, instance=project)

    if form.is_valid():
        form.save()
        return redirect("register")

    return render(request, "admin_allotment.html", {"form": form})


def upload_milestone(request):
    form = MilestoneForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect("upload")

    return render(request, "upload.html", {"form": form})


def evaluate_project(request):
    form = EvaluationForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect("evaluate")

    return render(request, "guide_evaluation.html", {"form": form})
