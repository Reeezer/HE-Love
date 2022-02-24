from django.db import models
from datetime import date
import base64


class Gender(models.Model):
    name = models.CharField(max_length=20)
    
    
class Interest(models.Model):
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.description


class User(models.Model):
    name = models.CharField(max_length=20)
    birth_date = models.DateField()
    gender = models.ForeignKey('Gender', on_delete=models.CASCADE, related_name='user_gender')
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
    def get_age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))


class Picture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='picture_user')

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
    
    
class Match(models.Model):
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_user_1')
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_user_2')
    date = models.DateField()
    last_message_date = models.DateField()
    
    class Meta:
        verbose_name_plural="Matches"
        
        
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
        verbose_name_plural="User_interests"



