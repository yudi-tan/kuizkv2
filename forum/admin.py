from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import Forum, Forumpost, Comment

admin.site.register(Forum)
admin.site.register(Forumpost)
admin.site.register(Comment)


