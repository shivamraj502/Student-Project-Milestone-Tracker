from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
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


def export_projects_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="projects_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Domain', 'Team Members', 'Marks', 'Publication Status', 'Guide'])

    projects = Project.objects.all()

    domain = request.GET.get('domain')
    guide_id = request.GET.get('guide_id')
    publication_status = request.GET.get('publication')

    if domain:
        projects = projects.filter(domain__iexact=domain)
    if guide_id:
        projects = projects.filter(guide_id=guide_id)
    if publication_status:
        is_published = publication_status.lower() == 'true'
        projects = projects.filter(evaluation__publication_status=is_published)

    for project in projects.distinct():
        team_members = filter(None, [project.student1_name, project.student2_name, project.student3_name, project.student4_name])
        team_str = ", ".join(team_members)
        
        evaluations = project.evaluation_set.all()
        marks = evaluations.first().marks if evaluations.exists() else 'N/A'
        pub_status = 'Yes' if (evaluations.exists() and evaluations.first().publication_status) else 'No'
        guide_name = project.guide.name if project.guide else 'Unassigned'
        
        writer.writerow([project.title, project.domain, team_str, marks, pub_status, guide_name])

    return response

