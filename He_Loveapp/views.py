from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic, View
from django.urls import reverse_lazy

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django import forms
import datetime

from .models import AppUser, Gender
from django.contrib.auth import get_user_model

# Create your wiews here


@login_required
def index(request):
    return render(request, 'He_Loveapp/index.html')


def sign_up(request):
    context = {}
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'He_Loveapp/index.html')
    context['form'] = form
    return render(request, 'registration/sign_up.html', context)


@login_required
class UserListView(generic.ListView):
    model = AppUser

    def get_queryset(self):
        return AppUser.objects.all()


@login_required
class UserDetailView(generic.DetailView):
    model = AppUser


class RegisterForm(UserCreationForm):
    birth_date = forms.DateField(initial=datetime.date.today, label='Birth date')
    #description = forms.CharField(widget=forms.Textarea, label='Description')
    #gender = forms.MultipleChoiceField(widget=forms.RadioSelect, choices=Gender.values(), label='Gender')

    class Meta:
        model = AppUser
        fields = ['username', 'password1', 'password2', 'birth_date', 'gender', 'description']

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.birth_date = self.cleaned_data['birth_date']
        user.gender = self.cleaned_data['gender']
        user.description = self.cleaned_data['description']
        if commit:
            user.save()
        return user


@login_required
class UserUpdateView(generic.UpdateView):
    model = AppUser
    fields = ['name', 'birth_date', 'gender', 'description']
    success_url = reverse_lazy('users-list')
