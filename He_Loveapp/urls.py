from django.urls import path

from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='home'),
    path('temp/', views.tempTestView, name='temp'),
    path('accounts/sign_up/', views.sign_up, name='sign-up'),
    path('users/', views.UserListView.as_view(), name='users-list'),
    path('users/<pk>/', views.UserDetailView.as_view(), name='users-detail'),
    path('users/<pk>/update/', views.update_user, name='users-update'),
    path('users/<pk>/like/', views.like, name='users-like'),
    path('users/<pk>/superlike/', views.superlike, name='users-superlike'),
    path('users/<pk>/dislike/', views.dislike, name='users-dislike'),
    path('events/', views.EventListView.as_view(), name='events-list'),
    path('events/create/', views.EventCreateView.as_view(), name='events-create'),
    path('events/<pk>/', views.EventDetailView.as_view(), name='events-detail'),
    path('events/<pk>/update/', views.EventUpdateView.as_view(), name='events-update'),
    path('events/<pk>/delete/', views.EventDeleteView.as_view(), name='events-delete'),
    path('chat/', views.MatchListView.as_view(), name='chat'),
    path('chat/<str:room_name>/', views.room, name='room'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
