from django.db import models
from authentication.models import User


class Project(models.Model):
    projectname = models.CharField(
        max_length=200)
    users = models.ManyToManyField(
        User,
        through='ProjectUser')
    projectowner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projectowner',
        default=1)


class Right(models.Model):
    name = models.CharField(
        max_length=200)
    description = models.CharField(
        max_length=1000)


class ProjectUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE)
    rights = models.ManyToManyField(
        Right)


class File(models.Model):
    uploader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uploader')
    table = models.CharField(
        max_length=100000)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE)


class Chat(models.Model):
    Project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE)
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    message = models.CharField(
        max_length=10000)
    timestamp = models.TimeField(
        auto_now=True)


class Scheme(models.Model):
    Creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    Project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE)
    schemejson = models.CharField(
        max_length=100000)


class Dataset(models.Model):
    Uploader = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    Project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE)
    datasetjson = models.CharField(
        max_length=100000)
