from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from projects.models import Task, Project
from users.models import User


class TaskSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'due_date',
            'status',
            'developer',
            'project',
        )


class CreateTaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'due_date',
            'developer',
        )

    def validate(self, attrs):
        user = attrs.get('developer')
        if user.is_developer:
            if user in Project.objects.get(id=self.context['view'].kwargs['project_id']).members.all():
                return attrs
            else:
                raise serializers.ValidationError('Assigned user must be project member.')
        else:
            raise serializers.ValidationError('Assigned user must be developer.')

    def create(self, validated_data):
        task = Task(title=validated_data.get('title'),
                    description=validated_data.get('description'),
                    due_date=validated_data.get('due_date'),
                    developer=validated_data.get('developer'),
                    project_id=self.context['view'].kwargs['project_id']
                    )
        task.save()
        return task


class TaskDetailViewSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'due_date',
            'status',
            'developer',
            'project',
        )
        read_only_fields = (
            'id',
            'project'
        )

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():

            if attr != 'status' and getattr(instance, attr) != value and self.context['request'].user.is_developer:
                raise serializers.ValidationError('You can change only task status as developer.')
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

