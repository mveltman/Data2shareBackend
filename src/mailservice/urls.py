from rest_framework import routers
from .viewsets import MailViewSet

router = routers.DefaultRouter()
router.register('api/mail', MailViewSet, 'mails')

urlpatterns = router.urls
