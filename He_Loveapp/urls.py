from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.UserListView.as_view(), name='users-list'),
    path('users/<pk>/', views.UserDetailView.as_view(), name='users-detail'),
]