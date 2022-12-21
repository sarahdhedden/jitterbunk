from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from django.urls import path

from . import views

app_name = 'jitter'
urlpatterns = [
    path('', views.UserListView.as_view(), name='users'),
    path('users', views.UserListView.as_view(), name='users'),
    path('bunks', views.BunkView.as_view(), name='all_bunks'),
    path('user/<int:user_id>', views.UserBunkView.as_view(), name='user_page'),
    path('<int:user_id>/bunk/', views.add_bunk, name='add_bunk'),
    path('accounts/signup', views.SignUpView.as_view(), name='signup'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/profile/", views.update_profile, name="update_profile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
