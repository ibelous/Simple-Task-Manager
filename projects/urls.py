from django.urls import path, include

from projects.views import project_views, task_views

app_name = 'projects'

task_patterns = [
    path('tasks/', task_views.TaskListAPIView.as_view(), name="tasks_list"),
    path('tasks/create/', task_views.TaskCreateAPIView.as_view(), name="create_task"),
    path('tasks/<pk>/', task_views.TaskDetailView.as_view(), name="task_details"),
]

urlpatterns = [
    path('projects/', project_views.ProjectListAPIView.as_view(), name="projects_list"),
    path('projects/create/', project_views.ProjectCreateAPIView.as_view(), name="create_project"),
    path('projects/<pk>/', project_views.ProjectDetailView.as_view(), name="project_details"),
    path('projects/<int:project_id>/', include(task_patterns)),
]
