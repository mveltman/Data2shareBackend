from django.db import models


class Datatransfer(models.Model):
    link = models.CharField(max_length=200)
