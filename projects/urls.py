from django.urls import path
from projects.views import project_views

app_name = 'projects'

urlpatterns = [
    path('projects/', project_views.ProjectListAPIView.as_view(), name="projects_list"),
    path('projects/create/', project_views.ProjectCreateAPIView.as_view(), name="create_project"),
    path('projects/<pk>/', project_views.ProjectDetailView.as_view(), name="project_details"),
]
