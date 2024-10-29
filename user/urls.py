# user/urls.py
from django.contrib.auth import views as auth_views
from django.urls import path
from user import views
from django.views.generic import TemplateView

app_name = 'users'


urlpatterns = [
    path('registration/', views.UserRegistration.as_view(), name='registration'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('posts/', views.user_posts, name='user_posts'),
    path('create_post/', views.CreatePostView.as_view(), name='create_post'),
    path('mis-publicaciones/', views.user_posts, name='user_posts'),
]