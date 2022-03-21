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
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *



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

@login_required
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

@login_required
def like(request, pk):
    swipe(request.user.id, pk, True)
    return redirect('users-list')
    
@login_required
def dislike(request, pk):
    swipe(request.user.id, pk, False)
    return redirect('users-list')

@login_required
def superlike(request, pk):
    # Superlike directly create a positive match between two people
    swipe(request.user.id, pk, True)
    swipe(pk, request.user.id, True)
    return redirect('users-list')

class UserListView(LoginRequiredMixin, generic.ListView):
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


class UserDetailView(LoginRequiredMixin, generic.DetailView):
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


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = AppUser
    fields = ['username', 'birth_date', 'gender', 'description']
    success_url = reverse_lazy('users-list')


class PictureListView(LoginRequiredMixin, generic.ListView):
    model = Picture

    def get_queryset(self):
        return Picture.objects.all()


class PictureDetailView(LoginRequiredMixin, generic.DetailView):
    model = Picture


class PictureCreateView(LoginRequiredMixin, generic.CreateView):
    model = Picture
    fields = ['picture_user', 'file']
    success_url = reverse_lazy('pictures-list')


class PictureUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Picture
    fields = ['picture_user', 'file']
    success_url = reverse_lazy('pictures-list')


class PictureDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Picture
    success_url = reverse_lazy('pictures-list')


class EventListView(LoginRequiredMixin, generic.ListView):
    model = Event

    def get_queryset(self):
        return Event.objects.all()


class EventDetailView(LoginRequiredMixin, generic.DetailView):
    model = Event


class EventCreateView(LoginRequiredMixin, generic.CreateView):
    model = Event
    fields = ['title', 'date', 'description']
    success_url = reverse_lazy('events-list')


class EventUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Event
    fields = ['title', 'date', 'description']
    success_url = reverse_lazy('events-list')


class EventDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Event
    success_url = reverse_lazy('events-list')


class MatchListView(LoginRequiredMixin, generic.ListView):
    model = Match

    def get_queryset(self):
        return Match.objects.all()


class MatchDetailView(LoginRequiredMixin, generic.DetailView):
    model = Match


class MatchCreateView(LoginRequiredMixin, generic.CreateView):
    model = Match
    fields = ['match_user_1', 'match_user_2', 'vote_user_1', 'vote_user_2', 'date', 'last_message_date']
    success_url = reverse_lazy('matchs-list')


class MatchUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Match
    fields = ['match_user_1', 'match_user_2', 'vote_user_1', 'vote_user_2', 'date', 'last_message_date']
    success_url = reverse_lazy('matchs-list')


class MatchDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Match
    success_url = reverse_lazy('matchs-list')


class ChatListView(LoginRequiredMixin, generic.ListView):
    model = Chat

    def get_queryset(self):
        return Chat.objects.all()


class ChatDetailView(LoginRequiredMixin, generic.DetailView):
    model = Chat


class ChatCreateView(LoginRequiredMixin, generic.CreateView):
    model = Chat
    fields = ['chat_user_sender', 'chat_user_receiver', 'message', 'date']
    success_url = reverse_lazy('chats-list')


class ChatUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Chat
    fields = ['chat_user_sender', 'chat_user_receiver', 'message', 'date']
    success_url = reverse_lazy('chats-list')


class ChatDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Chat
    success_url = reverse_lazy('chats-list')
