from django.db import models

# Create your models here.


class Guide(models.Model):
    name = models.CharField(max_length=100)

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
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    stage = models.CharField(max_length=100)
    file = models.FileField(upload_to="reports/")


class Evaluation(models.Model):
    RATING_CHOICES = [
        ("Excellent", "Excellent"),
        ("Good", "Good"),
        ("Average", "Average"),
        ("Needs Improvement", "Needs Improvement"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    guide_rating = models.CharField(max_length=30, choices=RATING_CHOICES)
    comments = models.TextField()
    publication_status = models.BooleanField(default=False)
