from django.db import models

# Create your models here.


class Guide(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200, unique=True)
    domain = models.CharField(max_length=100)
    team_members = models.TextField()
    guide = models.ForeignKey(Guide, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class Milestone(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    stage = models.CharField(max_length=100)
    file = models.FileField(upload_to="reports/")


class Evaluation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    guide_rating = models.IntegerField()
    comments = models.TextField()
    publication_status = models.BooleanField(default=False)
    certificate_copy = models.FileField(upload_to="reports/", null=True, blank=True)
