from django.contrib import admin

# Register your models here.
from .models import Course, Assignment, StudyTask
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(StudyTask)