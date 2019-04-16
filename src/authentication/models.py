from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Project(models.Model):
    projectname = models.CharField(max_length=200)
    users = models.ManyToManyField(User, through='ProjectUser')
    projectowner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projectowner', default=1)

class Right(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)

class ProjectUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    rights = models.ManyToManyField(Right)