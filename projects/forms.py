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
            "guide",
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

    def clean_file(self):
        file = self.cleaned_data.get('file', False)
        if file:
            if file.size > 50 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 50MB.")
        return file


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ["project", "guide_rating", "marks", "comments", "publication_status", "certificate_copy"]
        labels = {"publication_status": "Ready for Publication"}
        widgets = {
            "comments": forms.Textarea(
                attrs={"placeholder": "Enter faculty remarks here..."}
            )
        }

class CoordinatorApprovalForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ["coordinator_approval"]
