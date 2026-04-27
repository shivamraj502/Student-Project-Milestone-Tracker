from django import forms
from .models import Project, Milestone, Evaluation


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "domain", "team_members"]


class GuideAllotmentForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["guide"]


class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ["project", "stage", "file"]


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = [
            "project",
            "guide_rating",
            "comments",
            "publication_status",
            "certificate_copy",
        ]
