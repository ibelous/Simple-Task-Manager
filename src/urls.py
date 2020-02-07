from django.contrib import admin
from django.urls import path, include

from .swagger_urls import swagger_urlpatterns

api_urls = [
    path('', include('users.urls')),
    path('', include('projects.urls')),
    path('', include(swagger_urlpatterns)),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
]