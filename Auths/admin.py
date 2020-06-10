from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import MyUser
# Register your models here.

admin.site.register(MyUser)
admin.site.register(Permission)