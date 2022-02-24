from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic, View
from django.urls import reverse_lazy

from .models import User, Gender
from django.contrib.auth import get_user_model

# Create your wiews here

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class UserListView(generic.ListView):
    model = User

    def get_queryset(self):
        return User.objects.all()
    
class UserDetailView(generic.DetailView):
    model = User