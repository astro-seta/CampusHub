from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('club_manager', 'Club Manager'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

    def is_student(self):
        return self.role == 'student'

    def is_club_manager(self):
        return self.role == 'club_manager'

    def is_admin(self):
        return self.role == 'admin'