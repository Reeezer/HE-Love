from asyncio.windows_events import NULL
from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.db.models import Q
import base64
import datetime

class Gender(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
    
class Interest(models.Model):
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.description


class AppUser(User):
    birth_date = models.DateField(blank=False, default=datetime.datetime.now)
    gender = models.ForeignKey('Gender', on_delete=models.CASCADE, related_name='user_gender', blank=False, default=6)
    description = models.TextField(blank=False, default="Hello !")
    
    def __str__(self):
        return self.username
    
    def get_age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
    
    def get_interests(self):
        return User_interest.objects.filter(user=self.id)
    
    def get_gender_interests(self):
        return User_gender_interest.objects.filter(user=self.id)
    
    def get_matches(self):
        return Match.objects.filter(user_1=self.id).filter(user_2=self.id)


class Picture(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='picture_user')
    _file = models.TextField(db_column="file", blank=True)
    
    class Meta:
        verbose_name_plural="Pictures"

    def set_file(self, file):
        self._file = base64.encodestring(file)

    def get_file(self):
        return base64.decodestring(self._file)

    data = property(get_file, set_file)



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
    user_1 = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='match_user_1')
    user_2 = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='match_user_2')
    vote_user_1 = models.BooleanField(null=True)
    vote_user_2 = models.BooleanField(null=True)
    date = models.DateField(default=datetime.datetime.now)
    last_message_date = models.DateField(default=datetime.datetime.now)
    
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
    
    def get_opposite_user(self, user):
        if user == self.user_1:
            return self.user_2
        else:
            return self.user_1
        
    def contains_user(self, user_id):
        return user_id == self.user_1 or user_id == self.user_2
    
    def swipe(self, user_id, is_like):
        if user_id == self.user_1:
            self.vote_user_1 = is_like
        elif user_id == self.user_2:
            self.vote_user_2 = is_like
            
        if self.vote_user_1 == True and self.vote_user_2 == True:
            Chat.objects.create(user_sender=user_id, user_receiver=self.get_opposite_user(user_id), message="Entered in a new chat")
        # TODO check and do something if it's a match
        
    @classmethod
    def create(self, user_1, user_2, vote_user_1):
        self.user_1 = user_1
        self.user_2 = user_2
        self.vote_user_1 = vote_user_1
        self.date = datetime.datetime.now
        
        
class Chat(models.Model):
    user_sender = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='chat_user_sender')
    user_receiver = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='chat_user_receiver')
    message = models.TextField()
    date = models.DateField(default=datetime.datetime.now)
    
    class Meta:
        verbose_name_plural="Chats"
      

class User_interest(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='user_interest_user', default=1)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, related_name='user_interest_interest', default=1)
    
    class Meta:
        verbose_name_plural="User_interests"
        

class User_gender_interest(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='user_gender_interest_user', default=1)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, related_name='user_gender_interest_gender', default=1)
    
    class Meta:
        verbose_name_plural="User_gender_interests"



