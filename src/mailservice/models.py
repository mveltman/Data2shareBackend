from django.db import models
from project.models import Project


class Mail(models.Model):
    projectid = models.ForeignKey(Project, on_delete=models.CASCADE)
    key = models.CharField(max_length=40)
    target = models.CharField(max_length=100)
    link = models.CharField(max_length=200)
