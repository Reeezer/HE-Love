from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic, View
from django.urls import reverse_lazy

from .models import User, Gender
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
