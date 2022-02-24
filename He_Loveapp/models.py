from django.db import models
from datetime import date

class Gender(models.Model):
    name = models.CharField(max_length=20)

class User(models.Model):
    name = models.CharField(max_length=20)
    birth_date = models.DateField()
    gender = models.ForeignKey('Gender', on_delete=models.CASCADE)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
    def get_age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
