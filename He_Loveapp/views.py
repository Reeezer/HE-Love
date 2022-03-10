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

from .models import Picture, AppUser, Gender, Event, Match, Chat

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


class UserListView(generic.ListView):
    model = AppUser

    def get_queryset(self):
        return AppUser.objects.all()

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


class UserUpdateView(generic.UpdateView):
    model = AppUser
    fields = ['name', 'birth_date', 'gender', 'description']
    success_url = reverse_lazy('users-list')




class PictureListView(generic.ListView):
    model = Picture
    
    def get_queryset(self):
        return Picture.objects.all()

class PictureDetailView(generic.DetailView):
    model = Picture
    
class PictureCreateView(generic.CreateView):
    model = Picture
    fields = ['picture_user','file']
    success_url = reverse_lazy('pictures-list')
    
class PictureUpdateView(generic.UpdateView):
    model = Picture
    fields = ['picture_user','file']
    success_url = reverse_lazy('pictures-list')
    
class PictureDeleteView(generic.DeleteView):
    model = Picture
    success_url = reverse_lazy('pictures-list')





class EventListView(generic.ListView):
    model = Event
    
    def get_queryset(self):
        return Event.objects.all()

class EventDetailView(generic.DetailView):
    model = Event
    
class EventCreateView(generic.CreateView):
    model = Event
    fields = ['title','date','description']
    success_url = reverse_lazy('events-list')
    
class EventUpdateView(generic.UpdateView):
    model = Event
    fields = ['title','date','description']
    success_url = reverse_lazy('events-list')
    
class EventDeleteView(generic.DeleteView):
    model = Event
    success_url = reverse_lazy('events-list')
    
    
    
class MatchListView(generic.ListView):
    model = Match
    
    def get_queryset(self):
        return Match.objects.all()
        
class MatchDetailView(generic.DetailView):
    model = Match
    
class MatchCreateView(generic.CreateView):
    model = Match
    fields = ['match_user_1','match_user_2','vote_user_1','vote_user_2','date','last_message_date']
    success_url = reverse_lazy('matchs-list')
    
class MatchUpdateView(generic.UpdateView):
    model = Match
    fields = ['match_user_1','match_user_2','vote_user_1','vote_user_2','date','last_message_date']
    success_url = reverse_lazy('matchs-list')
    
class MatchDeleteView(generic.DeleteView):
    model = Match
    success_url = reverse_lazy('matchs-list')
    
    
    
class ChatListView(generic.ListView):
    model = Chat
    
    def get_queryset(self):
        return Chat.objects.all()
        
class ChatDetailView(generic.DetailView):
    model = Chat
    
class ChatCreateView(generic.CreateView):
    model = Chat
    fields = ['chat_user_sender','chat_user_receiver','message','date']
    success_url = reverse_lazy('chats-list')
    
class ChatUpdateView(generic.UpdateView):
    model = Chat
    fields = ['chat_user_sender','chat_user_receiver','message','date']
    success_url = reverse_lazy('chats-list')
    
class ChatDeleteView(generic.DeleteView):
    model = Chat
    success_url = reverse_lazy('chats-list')