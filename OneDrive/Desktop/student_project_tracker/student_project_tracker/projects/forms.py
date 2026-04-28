from django import forms
from .models import Project, Milestone, Evaluation


from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "domain",
            "student1_name",
            "student1_usn",
            "student2_name",
            "student2_usn",
            "student3_name",
            "student3_usn",
            "student4_name",
            "student4_usn",
        ]


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
        fields = ["project", "guide_rating", "comments", "publication_status"]
        labels = {"publication_status": "Ready for Publication"}
        widgets = {
            "comments": forms.Textarea(
                attrs={"placeholder": "Enter faculty remarks here..."}
            )
        }
