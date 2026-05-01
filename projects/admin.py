from django.contrib import admin

from .models import Evaluation, Guide, Milestone, Project


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    search_fields = ("name", "user__username")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "domain", "guide", "created_by")
    search_fields = ("title", "domain", "student1_usn", "student2_usn")
    list_filter = ("domain", "guide")


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ("project", "stage", "uploaded_by")
    list_filter = ("stage",)


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ("project", "guide_rating", "marks", "publication_status", "evaluated_by")
    list_filter = ("guide_rating", "publication_status", "coordinator_approval")
