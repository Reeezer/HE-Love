from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('accounts/sign_up/', views.sign_up, name='sign-up'),
    path('users/', views.UserListView.as_view(), name='users-list'),
    path('users/<pk>/', views.UserDetailView.as_view(), name='users-detail'),
    path('users/<pk>/update/', views.UserUpdateView.as_view(), name='users-update'),
]
