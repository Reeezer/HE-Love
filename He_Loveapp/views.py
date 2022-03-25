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
from django.db.models import Q
from django.shortcuts import redirect

from .models import Picture, AppUser, Gender, Event, Match, Chat, User_interest, User_gender_interest



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
            return redirect('home')
    context['form'] = form
    return render(request, 'registration/sign_up.html', context)


def swipe(request_id, pk, is_like):
    user_2 = AppUser.objects.get(id=pk)
    user_1 = AppUser.objects.get(id=request_id)
    
    if is_like == True:
        user_2.rank_up(1)
    
    # if the match already exists (the other user has already liked or disliked you), only modify it
    if Match.objects.filter((Q(user_1=user_1.id) | Q(user_2=user_1.id)) & (Q(user_1=user_2) | Q(user_2=user_2))).exists():
        match = Match.objects.get((Q(user_1=user_1.id) | Q(user_2=user_1.id)) & (Q(user_1=user_2) | Q(user_2=user_2)))
        match.swipe(user_1, is_like)
        match.save()
        # TODO maybe set the pair user_1, user_2 as unique in this table
    # if the match doesn't exists, let's create it
    else:
        Match.objects.create(user_1=user_1, user_2=user_2, vote_user_1=is_like)

def like(request, pk):
    swipe(request.user.id, pk, True)
    return redirect('users-list')
    
def dislike(request, pk):
    swipe(request.user.id, pk, False)
    return redirect('users-list')

def superlike(request, pk):
    # Superlike directly create a positive match between two people
    swipe(request.user.id, pk, True)
    swipe(pk, request.user.id, True)
    return redirect('users-list')

class UserListView(generic.ListView):
    model = AppUser

    def get_queryset(self):
        current_user = AppUser.objects.get(id=self.request.user.id)
        
        gender_interests = User_gender_interest.objects.filter(user=current_user.id).values('gender')        
        genders = Gender.objects.filter(id__in=gender_interests)
        
        # We don't want to see again:
        # People that we already liked
        matches_1 = Match.objects.filter((Q(user_1=current_user) & Q(vote_user_1=True)) | (Q(user_2=current_user) & Q(vote_user_2=True))).values('user_1')
        matches_2 = Match.objects.filter((Q(user_1=current_user) & Q(vote_user_1=True)) | (Q(user_2=current_user) & Q(vote_user_2=True))).values('user_2')
        # People who we already have a match with
        matches_3 = Match.objects.filter((Q(user_2=current_user) | Q(user_1=current_user)) & ~Q(vote_user_1=None) & ~Q(vote_user_2=None)).values('user_1')
        matches_4 = Match.objects.filter((Q(user_2=current_user) | Q(user_1=current_user)) & ~Q(vote_user_1=None) & ~Q(vote_user_2=None)).values('user_2')
        
        return AppUser.objects.filter(gender__in=genders).exclude(id=current_user.id).exclude(Q(id__in=matches_1) | Q(id__in=matches_2) | Q(id__in=matches_3) | Q(id__in=matches_4)).order_by('-rank')


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
    fields = ['username', 'birth_date', 'gender', 'description']
    success_url = reverse_lazy('users-list')


class PictureListView(generic.ListView):
    model = Picture

    def get_queryset(self):
        return Picture.objects.all()


class PictureDetailView(generic.DetailView):
    model = Picture


class PictureCreateView(generic.CreateView):
    model = Picture
    fields = ['picture_user', 'file']
    success_url = reverse_lazy('pictures-list')


class PictureUpdateView(generic.UpdateView):
    model = Picture
    fields = ['picture_user', 'file']
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
    fields = ['title', 'date', 'description']
    success_url = reverse_lazy('events-list')


class EventUpdateView(generic.UpdateView):
    model = Event
    fields = ['title', 'date', 'description']
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
    fields = ['match_user_1', 'match_user_2', 'vote_user_1', 'vote_user_2', 'date', 'last_message_date']
    success_url = reverse_lazy('matchs-list')


class MatchUpdateView(generic.UpdateView):
    model = Match
    fields = ['match_user_1', 'match_user_2', 'vote_user_1', 'vote_user_2', 'date', 'last_message_date']
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
    fields = ['chat_user_sender', 'chat_user_receiver','chat_match', 'message', 'date']
    success_url = reverse_lazy('chats-list')


class ChatUpdateView(generic.UpdateView):
    model = Chat
    fields = ['chat_user_sender', 'chat_user_receiver','chat_match', 'message', 'date']
    success_url = reverse_lazy('chats-list')


class ChatDeleteView(generic.DeleteView):
    model = Chat
    success_url = reverse_lazy('chats-list')
    
@login_required    
def chat_choose(request):
    return render(request, 'He_Loveapp/chat.html')

@login_required
def room(request, room_name):
    ## splitting the room_name to get the two users username
    users = room_name.split("m4t5hW1t3h")
    
    users_1 = AppUser.objects.get(username=users[0])
    f = open("log.txt","w")
    f.write(f"\nrequest.user : {request.user}\n")
    f.write(f"\nuser_1 : {users_1}\n")
    users_2 = AppUser.objects.get(username=users[1])
    f.write(f"user_2 : {users_2}\n")
    
    # A user can only go in a room matching :
    if str(request.user) == str(users_1) or str(request.user) == str(users_2) :
        match = Match.objects.get((Q(user_1 = users_1) & Q(user_2 = users_2))  | (Q(user_1 = users_2) & Q(user_2 = users_1)))
        f.write(f"matches : {match}\n")
        chats = Chat.objects.filter(Q(match = match))
        f.write(f"chat : {chats}\n")
        f.close()
        return render(request, 'He_Loveapp/room.html', {
            'room_name': room_name,
            'users_1' : users_1,
            'users_2' : users_2,
            'chats' : chats,
            'match' : match
        })
    else :  
        return render(request, 'He_Loveapp/index.html')
