from django.urls import path
from . import views

app_name = 'jitter'
urlpatterns = [
    path('', views.UserListView.as_view(), name='login'),
    path('users', views.UserListView.as_view(), name='users'),
    path('bunks', views.BunkView.as_view(), name='bunks'),
    path('user/<int:user_id>', views.UserBunkView.as_view(), name='user'),
    path('<int:user_id>/bunk/', views.add_bunk, name='add_bunk')
] 
