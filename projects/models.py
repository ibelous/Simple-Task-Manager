from django.db import models

import datetime

from users.models import User

# Create your models here.


class Project(models.Model):
    PROJECT_STATUSES = (
        ('Opened', 'Opened'),
        ('Closed', 'Closed'),
    )

    title = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=3000)
    status = models.CharField(choices=PROJECT_STATUSES, max_length=10, default='Opened')
    members = models.ManyToManyField(User, related_name='projects')

    def __str__(self):
        return self.title


class Task(models.Model):
    TASK_STATUSES = (
        ('To do', 'To do'),
        ('In progress', 'In progress'),
        ('Done', 'Done'),
    )

    title = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=3000)
    due_date = models.DateTimeField(default=datetime.date.today()+datetime.timedelta(days=7))
    status = models.CharField(choices=TASK_STATUSES, max_length=15, default='To do')
    developer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title
