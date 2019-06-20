from rest_framework import viewsets
from .models import Mail
from .serializers import MailSerializer
from django.core import mail
from project.models import Project


class MailViewSet(viewsets.ModelViewSet):
    queryset = Mail.objects.all()
    serializer_class = MailSerializer

    def perform_create(self, serializer):
        obj = serializer.save()
        connection = mail.get_connection()
        connection.open()
        print(obj.projectid.projectname)
        email = mail.EmailMessage(
            'You have been invited to ' + obj.projectid.projectname,
            'You have been invited. <br>' +
            'You can join the project by following this link: ' + obj.link,
            '322685@student.fontys.nl',
            [obj.target],
        )
        email.content_subtype = 'html'
        email.send()
