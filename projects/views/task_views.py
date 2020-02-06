from projects.serializers.task_serializers import TaskDetailViewSerializer, TaskSerializer, CreateTaskSerializer
from projects.models import Task
from projects.permissions import *

from rest_framework import generics


class TaskListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    lookup_field = 'project_id'
    permission_classes = (IsTaskProjectMember, )

    def get_queryset(self):
        return Task.objects.filter(project_id=self.kwargs['project_id'])


class TaskCreateAPIView(generics.CreateAPIView):
    serializer_class = CreateTaskSerializer
    permission_classes = (IsManager, IsTaskProjectMember)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskDetailViewSerializer
    lookup_field = 'pk'
    permission_classes = (IsTaskProjectMember, IsTaskDeveloperOrManager)

    def get_queryset(self):
        return Task.objects.filter(project_id=self.kwargs['project_id'])

