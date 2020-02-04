from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    USER_TYPES = (
        ('Manager', 'Manager'),
        ('Developer', 'Developer'),
    )
    user_type = models.CharField(choices=USER_TYPES, max_length=10)
    email = models.EmailField(unique=True)

    @property
    def is_manager(self):
        return self.user_type == 'Manager'

    @property
    def is_developer(self):
        return self.user_type == 'Developer'
