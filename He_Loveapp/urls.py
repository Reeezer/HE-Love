from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.UserListView.as_view(), name='users-list'),
    path('users/create/', views.UserCreateView.as_view(), name='users-create'),
    path('users/<pk>/', views.UserDetailView.as_view(), name='users-detail'),
    path('users/<pk>/update/', views.UserUpdateView.as_view(), name='users-update'),

    path('events/', views.EventListView.as_view(), name='events-list'),
    path('events/create/', views.EventCreateView.as_view(), name='events-create'),
    path('events/<pk>/', views.EventDetailView.as_view(), name='events-detail'),
    path('events/<pk>/update/', views.EventUpdateView.as_view(), name='events-update'),
    path('events/<pk>/delete/', views.EventDeleteView.as_view(), name='events-delete'),


]