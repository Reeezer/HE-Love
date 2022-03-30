from urllib import request
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
from django.shortcuts import render

from .models import *

from django.core import serializers


# Create your wiews here


@login_required
def index(request):
    return redirect('users-list')

from .forms import ImageForm
def tempTestView(request):
    context = {}
    if request.method == 'POST':
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            img = form.cleaned_data.get("image")
            obj = Picture.objects.create(
                user = AppUser.objects.get(username=name),
                path = img
            )
            obj.save()
    else:
        form = ImageForm()
            
    
    context['form'] = ImageForm()
    return render(request,"He_Loveapp/picture_list.html",context)

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
def update_user(request, pk):
    if int(request.user.id) != int(pk):
        return redirect('users-detail', request.user.id)
    
    user = AppUser.objects.get(id=pk)
    user_interests = User_interest.objects.filter(user=user).values('interest')
    interests = Interest.objects.filter(id__in=user_interests).values('description')
    
    user_gender_interests = User_gender_interest.objects.filter(user=user).values('gender')
    gender_interests = Gender.objects.filter(id__in=user_gender_interests).values('name')
    
    form = UpdateUserForm(request.POST or None, instance=user)
    context = {'form': form, 'appuser':user, 'interests':list(interests), 'gender_interests':list(gender_interests)}
    if form.is_valid():
        obj = form.save()
        obj.save()
        return redirect('users-detail', request.user.id)
    return render(request, 'registration/sign_up.html', context)

def swipe(request_id, pk, is_like):
    user_2 = AppUser.objects.get(id=pk)
    user_1 = AppUser.objects.get(id=request_id)
    
    if is_like == True:
        user_2.rank_up(1)
    # if we put a dislike, we do want to not see this person anymore until 3 days
    elif is_like == False: 
        # if the dislike already exists, only modify it
        if Dislike.objects.filter(Q(user=user_1) & Q(user_disliked=user_2)).exists():
            dislike = Dislike.objects.get(Q(user=user_1) & Q(user_disliked=user_2))
            dislike.refresh()
            dislike.save()
            # TODO maybe set the pair user_1, user_2 as unique in this table
        # if the dislike doesn't exists, let's create it
        else:
            Dislike.objects.create(user=user_1, user_disliked=user_2)

    # if the match already exists (the other user has already liked or disliked you), only modify it
    if Match.objects.filter((Q(user_1=user_1.id) & Q(user_2=user_2.id)) | (Q(user_1=user_2.id) & Q(user_2=user_1.id))).exists():
        match = Match.objects.get((Q(user_1=user_1.id) & Q(user_2=user_2.id)) | (Q(user_1=user_2.id) & Q(user_2=user_1.id)))
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
        # People that we already disliked within 3 days
        disliked_users = Dislike.objects.filter(Q(user=current_user))
        disliked_3days = [disliked_user.user_disliked.id for disliked_user in disliked_users if not disliked_user.is_valid_now()]
        
        return AppUser.objects.filter(gender__in=genders).exclude(id=current_user.id).exclude(Q(id__in=matches_1) | Q(id__in=matches_2) | Q(id__in=matches_3) | Q(id__in=matches_4) | Q(id__in=disliked_3days)).order_by('rank')[:3]


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = AppUser


class RegisterForm(UserCreationForm):
    user_gender_interests = forms.ModelMultipleChoiceField(queryset=Gender.objects.all(), label='Genres recherchés', widget=forms.CheckboxSelectMultiple(attrs={'class': 'forms-box'}))
    user_interests = forms.ModelMultipleChoiceField(queryset=Interest.objects.all(), label="Intérêts", widget=forms.CheckboxSelectMultiple(attrs={'class': 'forms-box'}))

    class Meta:
        model = AppUser
        fields = ['username', 'password1', 'password2', 'birth_date', 'gender', 'description']

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
        gender_interests = self.cleaned_data['user_gender_interests']
        user_interests = self.cleaned_data['user_interests']
        
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



class EventListView(LoginRequiredMixin, generic.ListView):
    model = Event

    def get_queryset(self):
        return Event.objects.all()


class EventDetailView(LoginRequiredMixin, generic.DetailView):
    model = Event


class EventCreateView(LoginRequiredMixin, generic.CreateView):
    model = Event
    fields = ['title', 'date',  'description','image']
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
        return Match.objects.filter((Q(user_1=self.request.user.id) | Q(user_2=self.request.user.id)) & Q(vote_user_1=True) & Q(vote_user_2=True)).order_by('-last_message_date')


class ChatListView(LoginRequiredMixin, generic.ListView):
    model = Chat

    def get_queryset(self):
        return Chat.objects.all()

@login_required
def room(request, room_name):
    ## splitting the room_name to get the two users username
    users = room_name.split("m4t5hW1t3h")
    
    ## Checking if user_1 exists
    try:
        user_1 = AppUser.objects.get(username=users[0])
    except:
        user_1 = None
        
    ## Checking if user_2 exists
    try:
        user_2 = AppUser.objects.get(username=users[1])
    except:
        user_2 = None    
    
    # A user can only go in a room matching :
    if str(request.user) == str(user_1) or str(request.user) == str(user_2):
        try:
            match = Match.objects.get((Q(user_1=user_1.id) & Q(user_2=user_2.id)) | (Q(user_1=user_2.id) & Q(user_2=user_1.id)))
        except:
            match = None
            
        if match != None:
            chats = Chat.objects.filter(Q(match = match))

            return render(request, 'He_Loveapp/room.html', {
                'room_name': room_name,
                'users_1' : user_1,
                'users_2' : user_2,
                'chats' : chats,
                'match' : match
            })
        else:
            return redirect('chat')
    else :  
        return redirect('chat')
