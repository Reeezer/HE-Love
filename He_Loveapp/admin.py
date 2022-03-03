from django.contrib import admin

from .models import User, Gender, Interest,Picture,Event,Match,Chat,User_interest,User_gender_interest

# Register your models here.
admin.site.register(User)
admin.site.register(Gender)
admin.site.register(Interest)
admin.site.register(Picture)
admin.site.register(Event)
admin.site.register(Match)
admin.site.register(Chat)
admin.site.register(User_interest)
admin.site.register(User_gender_interest)
