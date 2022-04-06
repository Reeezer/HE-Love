from django import forms
from datetime import date
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Gender, Interest, AppUser, User_gender_interest, User_interest, Picture

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


class UpdateUserForm(LoginRequiredMixin, forms.ModelForm):
    user_gender_interests = forms.ModelMultipleChoiceField(queryset=Gender.objects.all(), label='Genres recherchés', widget=forms.CheckboxSelectMultiple(attrs={'class': 'forms-box'}))
    user_interests = forms.ModelMultipleChoiceField(queryset=Interest.objects.all(), label="Intérêts", widget=forms.CheckboxSelectMultiple(attrs={'class': 'forms-box'}))

    class Meta:
        model = AppUser
        fields = ['birth_date', 'gender', 'description']

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
