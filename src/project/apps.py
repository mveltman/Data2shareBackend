from django.apps import AppConfig
from .manager import ProjectManager


class ProjectConfig(AppConfig):
    name = 'project'
    manager = ProjectManager()
