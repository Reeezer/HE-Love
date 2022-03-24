from asyncio.windows_events import NULL
from django.db import models
from datetime import date
from django.contrib.auth.models import User
import base64

class Gender(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
    
class Interest(models.Model):
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.description

def user_Image_Files_directory_path(instance,filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    if isinstance(instance,AppUser):
        return f'userimages/user_{instance.id}/pp.{filename.split(".")[-1]}'
    else:
        return f'userimages/user_{instance.user.id}/pp.{filename.split(".")[-1]}'
    


class AppUser(User):
    birth_date = models.DateField()
    gender = models.ForeignKey('Gender', on_delete=models.CASCADE, related_name='user_gender')
    description = models.TextField()
    profilePicture = models.ImageField(upload_to=user_Image_Files_directory_path)
    
    def __str__(self):
        return self.username
    
    def get_age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))


class Picture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='picture_user')
    path = models.ImageField(upload_to =user_Image_Files_directory_path)
    
    class Meta:
        verbose_name_plural="Pictures"


class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()
    
    class Meta:
        verbose_name_plural="Events"
    
    def __str__(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_date(self):
        return self.date
    
    
class Match(models.Model):
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_user_1')
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_user_2')
    vote_user_1 = models.BooleanField(null=True)
    vote_user_2 = models.BooleanField(null=True)
    date = models.DateField()
    last_message_date = models.DateField()
    
    class Meta:
        verbose_name_plural="Matches"
        
    def check_match(self):
        # Both matches
        if self.vote_user_1 == True and self.vote_user_2 == True:
            return True, "It's a match !"
        
        # No match :(
        elif self.vote_user_1 == False or self.vote_user_2 == False:
           return False, "Match refused :("
       
        else:
            return False, "Waiting for match"
        
    def get_last_message_date(self):
        return self.last_message_date
    
    def get_matched_users(self):
        if self.check_match():
            return self.user_1, self.user_2
        
        
class Chat(models.Model):
    user_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_user_sender')
    user_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_user_receiver')
    message = models.TextField()
    date = models.DateField()
    
    class Meta:
        verbose_name_plural="Chats"
      

class User_interest(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_interest_user_id')
    interest_id = models.ForeignKey(Interest, on_delete=models.CASCADE, related_name='user_interest_interest_id')
    
    class Meta:
        verbose_name_plural="User_interests"
        

class User_gender_interest(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_gender_interest_user_id')
    gender_id = models.ForeignKey(Gender, on_delete=models.CASCADE, related_name='user_gender_interest_gender_id')
    
    class Meta:
        verbose_name_plural="User_gender_interests"



