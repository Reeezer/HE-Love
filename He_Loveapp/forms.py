from multiprocessing import Event
from django import forms
from datetime import date
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Gender, Interest, AppUser, User_gender_interest, User_interest, Picture,Event

import re

class ImageForm(forms.Form):
    image = forms.ImageField()
    name = forms.CharField()
    
class RegisterForm(UserCreationForm):
    user_picture_1 = forms.ImageField(label="Photo 1", required=False)
    user_picture_2 = forms.ImageField(label="Photo 2", required=False)
    user_picture_3 = forms.ImageField(label="Photo 3", required=False)
    user_picture_4 = forms.ImageField(label="Photo 4", required=False)
    user_gender_interests = forms.ModelMultipleChoiceField(queryset=Gender.objects.all(), label='Genres recherchés', widget=forms.CheckboxSelectMultiple(attrs={'class': 'forms-box'}))
    user_interests = forms.ModelMultipleChoiceField(queryset=Interest.objects.all(), label="Intérêts", widget=forms.CheckboxSelectMultiple(attrs={'class': 'forms-box'}))

    class Meta:
        model = AppUser
        fields = ['username', 'password1', 'password2', 'birth_date', 'gender', 'description', 'profile_picture']

    def clean_birth_date(self):
        dob = self.cleaned_data['birth_date']
        age = (date.today() - dob).days / 365
        if age < 18:
            raise forms.ValidationError('You must be at least 18 years old')
        return dob
    
    def clean_username(self):
        dou = self.cleaned_data['username']
        reg = re.compile('^[a-z0-9\._-]+$')
        if not reg.match(dou):
            raise forms.ValidationError('Seulement les charactères alphanumériques sont autorisés, ainsi que les caractères spéciaux: -, _, .')
        return dou
    
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
        
        gender_interests = self.cleaned_data['user_gender_interests']
        user_interests = self.cleaned_data['user_interests']
        pictures = []
        for i in range(1, 5):
            picture = self.cleaned_data[f"user_picture_{i}"]
            if picture:
                pictures.append(picture)
        
        for gender_interest in gender_interests:
            User_gender_interest.objects.create(user=user, gender=gender_interest)
        i = 0
        for interest in user_interests:
            if i < 5: 
                User_interest.objects.create(user=user, interest=interest)
                i += 1
        i = 0
        for picture in pictures:
            if i < 4: 
                Picture.objects.create(user=user, path=picture)
                i += 1
        
        if commit:
            user.save()
        return user


class EventCreationForm(LoginRequiredMixin,forms.ModelForm):
    title = forms.CharField(label="Titre", max_length=25,required=True)
    date = forms.DateField(label="Date", required=True)
    description = forms.CharField(label="Description", max_length=500, required=False)
    image = forms.ImageField(label="Image de l'event", required=False)
    
    class Meta:
        model = Event
        fields = ['title', 'date', 'description', 'image']
    
    def clean_date(self):
        doe = self.cleaned_data['date']
        days = (date.today() - doe).days
        if days > 0:
            raise forms.ValidationError('La date de l\'évènement doit être dans le futur')
        return doe
    
    def save(self,owner,commit=True):
        event = super(EventCreationForm, self).save(commit=False)
        event.owner = owner
        if commit:
            event.save()
        event.participants.add(owner.id)
        if commit:
            event.save()
        return event

class UpdateUserForm(LoginRequiredMixin, forms.ModelForm):
    user_gender_interests = forms.ModelMultipleChoiceField(queryset=Gender.objects.all(), label='Genres recherchés', widget=forms.CheckboxSelectMultiple(attrs={'class': 'forms-box'}))
    user_interests = forms.ModelMultipleChoiceField(queryset=Interest.objects.all(), label="Intérêts", widget=forms.CheckboxSelectMultiple(attrs={'class': 'forms-box'}))

    class Meta:
        model = AppUser
        fields = ['birth_date', 'gender', 'description', 'profile_picture']

    def save(self, commit=True):
        # it's not the right way to do this, but we're already too far in the project to change the database and add ManyToMany field in models
        user = super(UpdateUserForm, self).save(commit=False)
        if commit:
            user.save()
        gender_interests = self.cleaned_data['user_gender_interests']
        user_interests = self.cleaned_data['user_interests']
        
        User_gender_interest.objects.filter(user=user).delete()
        User_interest.objects.filter(user=user).delete()
        
        for gender_interest in gender_interests:
            User_gender_interest.objects.create(user=user, gender=gender_interest)
        i = 0
        for interest in user_interests:
            if i < 5: 
                User_interest.objects.create(user=user, interest=interest)
                i += 1
        
        if commit:
            user.save()
        return user
    

class JoinEventForm(forms.Form):
    event_id = forms.IntegerField()
