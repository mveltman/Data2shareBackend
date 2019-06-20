from rest_framework import routers
from .viewsets import UserViewSet, UserDetail, UserCreate


router = routers.DefaultRouter()
router.register('api/users', UserViewSet, 'users')
router.register('api/login', UserDetail, 'user')
router.register('api/register', UserCreate, 'createuser')

for url in router.urls:
    print(url, '\n')

urlpatterns = router.urls
