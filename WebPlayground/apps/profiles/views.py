from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.registration.models import Profile
from apps.profiles.serializers import ProfilesSerializer


class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    paginate_by = 10


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'

    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs['username'])


class ProfilesAPIView(APIView):
    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializer = ProfilesSerializer(profiles, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProfilesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
