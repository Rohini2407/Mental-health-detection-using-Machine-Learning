from django.contrib import admin
from .models import CreateUserForm, UserResponse, DoctorInfo

admin.site.register(UserResponse)
admin.site.register(DoctorInfo)
