from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserRegistrationAPIView.as_view(), name="registration"),
    path('login/', views.UserLoginAPIView.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('users/', views.UserListAPIView.as_view(), name="users_list"),
    path('users/<pk>/', views.UserDetailView.as_view(), name="user_details"),
]
