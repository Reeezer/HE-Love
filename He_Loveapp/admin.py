from django.contrib import admin

from .models import AppUser, Gender

# Register your models here.
admin.site.register(AppUser)
admin.site.register(Gender)