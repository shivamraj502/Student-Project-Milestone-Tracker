from django.contrib import admin

# Register your models here.
from .models import Project, Guide, Milestone, Evaluation

admin.site.register(Project)
admin.site.register(Guide)
admin.site.register(Milestone)
admin.site.register(Evaluation)
