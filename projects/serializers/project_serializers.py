from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

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

    def validate(self, attrs):
        managers = 0
        devs = 0
        for member in attrs.get('members'):
            if member.is_developer:
                devs += 1
            if member.is_manager:
                managers += 1
        if managers and devs:
            return attrs
        else:
            raise serializers.ValidationError('Project need to have at least one manager and one developer.')

    def create(self, validated_data):
        project = Project(title=validated_data.get('title'),
                          description=validated_data.get('description'))
        project.save()
        project.members.set(validated_data.get('members'))
        return project


class ProjectDetailViewSerializer(ModelSerializer):
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
