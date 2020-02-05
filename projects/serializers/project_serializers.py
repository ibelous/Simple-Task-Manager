from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.models import Token

from projects.models import Project


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'description',
            'status',
            'members',
        )


class CreateProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'title',
            'description',
            'members',
        )

    def create(self, validated_data):
        project = Project(title=validated_data.get('title'),
                          description=validated_data.get('description'))
        project.save()
        project.members.set(validated_data.get('members'))
        return project


class ProjectDetailView(ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'description',
            'status',
            'members',
            'tasks',
        )
