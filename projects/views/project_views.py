from projects.serializers.project_serializers import ProjectSerializer, CreateProjectSerializer, ProjectDetailView
from projects.models import Project
from projects.permissions import IsManager, IsProjectMember, SafeOnly

from rest_framework import generics


class ProjectListAPIView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = (SafeOnly, )
    queryset = Project.objects.all()


class ProjectCreateAPIView(generics.CreateAPIView):
    serializer_class = CreateProjectSerializer
    permission_classes = (IsManager, )


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectDetailView
    lookup_field = 'pk'
    queryset = Project.objects.all()
    permission_classes = (IsProjectMember, IsManager | SafeOnly, )
