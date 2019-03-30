from rest_framework import viewsets
from apps.registration.models import Profile
from .serializers import ProfilesSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfilesSerializer