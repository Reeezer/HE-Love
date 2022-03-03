from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic, View
from django.urls import reverse_lazy

from .models import Picture, User, Gender,Event,Match,Chat
from django.contrib.auth import get_user_model

# Create your wiews here

def index(request):
    context = {}
    return render(request, 'He_Loveapp/index.html', context)

class UserListView(generic.ListView):
    model = User

    def get_queryset(self):
        return User.objects.all()
    
class UserDetailView(generic.DetailView):
    model = User
    
class UserCreateView(generic.CreateView):
    model = User
    fields = ['name', 'birth_date', 'gender', 'description']
    success_url = reverse_lazy('users-list')
    
class UserUpdateView(generic.UpdateView):
    model = User
    fields = ['name', 'birth_date', 'gender', 'description']
    success_url = reverse_lazy('users-list')




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