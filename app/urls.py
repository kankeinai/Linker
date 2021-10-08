from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth.views import LoginView
    
from .utilities import MENU


def slugify(str):
    return "-".join(str.lower().split(" ")) + "/"

urlpatterns = [
    
    path('about/', views.send_page, name='About'),
    path('logout/', views.send_page, name='logout'),
    path('faq/', views.send_page, name='FAQ'),
    path('rules/', views.send_page, name='Rules'),
    path('logaut/', views.send_page, name='Log out'),
    path('contact/', views.send_page, name='Contact us'),
    
    path('', views.PostView.as_view(), name="Home"),
    
    url(r'^accounts/login/$', LoginView.as_view(template_name = 'registration/login.html'), name="login"),
    url(r'^accounts/logout/$', views.LogoutView.as_view(), name="logout"),
    url(r'^accounts/register/$', views.RegisterView.as_view(), name='registration'),
    url(r'^accounts/profile/$', views.ProfileView.as_view(), name="profile"),
    url(r'^accounts/profile/edit/$', views.EditProfileView.as_view(), name="edit_profile"), 
    
]