from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('users/register/', views.UserRegistrationAPIView.as_view(), name="registration"),
    path('users/login/', views.UserLoginAPIView.as_view(), name="login"),
    path('users/', views.UserListAPIView.as_view(), name="users_list"),
]
