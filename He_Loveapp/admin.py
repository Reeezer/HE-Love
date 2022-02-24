from django.contrib import admin

from .models import User, Gender

# Register your models here.
admin.site.register(User)
admin.site.register(Gender)