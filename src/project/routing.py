from django.urls import re_path
from .consumers import ProjectConsumer

websocket_urlpatterns = [
    re_path(r'^ws/project/$', ProjectConsumer),
]
