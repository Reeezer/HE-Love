from typing_extensions import Required
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

def user_Image_Files_directory_path(instance,filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    if isinstance(instance,AppUser):
        return f'userimages/user_{instance.id}/pp.{filename.split(".")[-1]}'
    else:
        return f'userimages/user_{instance.user.id}/pp.{filename.split(".")[-1]}'
    


class AppUser(User):
    birth_date = models.DateField(blank=False, default=datetime.datetime.now)
    gender = models.ForeignKey('Gender', on_delete=models.CASCADE, related_name='user_gender', blank=False, default=6)
    description = models.TextField(blank=False, default="Hello !", max_length=300)
    rank = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to=user_Image_Files_directory_path,default='userimages/defaultUserPP.png')

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
        return Match.objects.filter((Q(user_1=self.id) | Q(user_2=self.id)) & Q(vote_user_1=True) & Q(vote_user_2=True))
    
    def rank_up(self, amount):
        self.rank += amount
        self.save()
        
    def get_pictures(self):
        return Picture.objects.filter(user=self.id)
    
    def nb_pictures(self):
        return range(len(list(Picture.objects.filter(user=self.id))))
    


class Picture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='picture_user')
    path = models.ImageField(upload_to =user_Image_Files_directory_path)
    
    class Meta:
        verbose_name_plural="Pictures"

def event_upload(instance,filename):
    return f'eventimages/event_{instance.id}/eventPP.{filename.split(".")[-1]}'
        
class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()
    image = models.ImageField(default='eventimages/default-Event.png',upload_to=event_upload)
    participants = models.ManyToManyField(AppUser)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_owner')
    
    class Meta:
        verbose_name_plural="Events"
    
    def __str__(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_date(self):
        return self.date
    
    def getParticipantsId(self):
        return [u.id for u in self.participants.all()]
    
    def getParticipants(self):
        return self.participants.all()
    
    def get_nb_partipants(self):
        return self.participants.count()

    
class Match(models.Model):
    user_1 = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='match_user_1')
    user_2 = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='match_user_2')
    vote_user_1 = models.BooleanField(null=True)
    vote_user_2 = models.BooleanField(null=True)
    date = models.DateTimeField(default=datetime.datetime.now)
    last_message_date = models.DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        verbose_name_plural="Matches"
    
    def get_opposite_user(self, user):
        if user == self.user_1:
            return self.user_2
        else:
            return self.user_1
        
    def contains_user(self, user_id):
        return user_id == self.user_1 or user_id == self.user_2
    
    def swipe(self, user, is_like):        
        if user == self.user_1:
            self.vote_user_1 = is_like
        elif user == self.user_2:
            self.vote_user_2 = is_like
        else:
            return
            
        self.date = datetime.datetime.now()
        self.last_message_date = datetime.datetime.now()
        
        if self.vote_user_1 == True and self.vote_user_2 == True:
            self.user_1.rank_up(5)
            self.user_2.rank_up(5)
            Chat.objects.create(user_sender=user, user_receiver=self.get_opposite_user(user), match=self)
            
    def get_last_message(self):
        return Chat.objects.filter(match=self.id).order_by('-date').first()
    
    def get_match_url(self):
        return f"{self.user_1}m4t5hW1t3h{self.user_2}"
        
    @classmethod
    def create(self, user_1, user_2, vote_user_1):
        self.user_1 = user_1
        self.user_2 = user_2
        self.vote_user_1 = vote_user_1
        self.date = datetime.datetime.now()
        self.last_message_date = datetime.datetime.now()
        
    def updaterecord_last_message_date(id, message_date):
        update_match = Match.objects.get(id=id)
        update_match.last_message_date = message_date
        update_match.save()
        
        
class Chat(models.Model):
    user_sender = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='chat_user_sender')
    user_receiver = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='chat_user_receiver')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='chat_match')
    message = models.TextField()
    date = models.DateTimeField(default=datetime.datetime.now)
    
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


class Dislike(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='dislike_user', default=1)
    user_disliked = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='dislike_user_disliked', default=1)
    date = models.DateField(default=datetime.date.today)
    
    def refresh(self):
        self.date = datetime.date.today()
        
    def is_valid_now(self):
        return datetime.date.today() - self.date > datetime.timedelta(days=3)