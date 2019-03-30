from rest_framework import routers
from apps.profiles.viewsets import ProfileViewSet

router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet)