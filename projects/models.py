from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.


class Guide(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200, unique=True)
    domain = models.CharField(max_length=100)

    student1_name = models.CharField(max_length=100)
    student1_usn = models.CharField(max_length=20)

    student2_name = models.CharField(max_length=100)
    student2_usn = models.CharField(max_length=20)

    student3_name = models.CharField(max_length=100, blank=True)
    student3_usn = models.CharField(max_length=20, blank=True)

    student4_name = models.CharField(max_length=100, blank=True)
    student4_usn = models.CharField(max_length=20, blank=True)

    guide = models.ForeignKey(Guide, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class Milestone(models.Model):
    STAGE_CHOICES = [
        ("Synopsis", "Synopsis"),
        ("Phase 1", "Phase 1"),
        ("Phase 2", "Phase 2"),
        ("Final Report", "Final Report"),
        ("Publication", "Publication"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    stage = models.CharField(max_length=100, choices=STAGE_CHOICES)
    file = models.FileField(
        upload_to="reports/",
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'zip'])]
    )


class Evaluation(models.Model):
    RATING_CHOICES = [
        ("Excellent", "Excellent"),
        ("Good", "Good"),
        ("Average", "Average"),
        ("Needs Improvement", "Needs Improvement"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    guide_rating = models.CharField(max_length=30, choices=RATING_CHOICES)
    marks = models.IntegerField(null=True, blank=True)
    comments = models.TextField()
    coordinator_approval = models.BooleanField(default=False)
    publication_status = models.BooleanField(default=False)
    certificate_copy = models.FileField(upload_to="certificates/", null=True, blank=True)
