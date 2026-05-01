from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Evaluation, Guide, Milestone, Project
from .permissions import ROLE_GUIDE, assign_role, is_admin


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("autocomplete", "off")


class RoleAuthenticationForm(StyledFormMixin, AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class RoleSignUpForm(StyledFormMixin, UserCreationForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def __init__(self, *args, role, **kwargs):
        self.role = role
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email", "")
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        if commit:
            user.save()
            assign_role(user, self.role)
            if self.role == ROLE_GUIDE:
                guide_name = user.get_full_name().strip() or user.username
                guide = Guide.objects.filter(name=guide_name, user__isnull=True).first()
                if guide:
                    guide.user = user
                    guide.save(update_fields=["user"])
                else:
                    Guide.objects.create(name=guide_name, user=user)
        return user


class ProjectForm(StyledFormMixin, forms.ModelForm):
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


class GuideAllotmentForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ["guide"]


class MilestoneForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ["project", "stage", "file"]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = Project.objects.all().order_by("title")
        if user and not is_admin(user):
            queryset = queryset.filter(created_by=user)
        self.fields["project"].queryset = queryset

    def clean_file(self):
        file = self.cleaned_data.get("file", False)
        if file and file.size > 50 * 1024 * 1024:
            raise forms.ValidationError("File size must be under 50MB.")
        return file


class EvaluationForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ["project", "guide_rating", "marks", "comments", "publication_status", "certificate_copy"]
        labels = {"publication_status": "Ready for Publication"}
        widgets = {
            "comments": forms.Textarea(
                attrs={"placeholder": "Enter faculty remarks here..."}
            )
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = Project.objects.all().order_by("title")
        if user and not is_admin(user):
            guide_profile = getattr(user, "guide_profile", None)
            queryset = queryset.filter(guide=guide_profile) if guide_profile else queryset.none()
        self.fields["project"].queryset = queryset


class CoordinatorApprovalForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ["coordinator_approval"]
