from django.contrib.auth.signals import user_logged_in
from django.contrib.sessions.models import Session
from django.conf import settings
from django.db import models

INTERESTS = (("all", "All"),
    ("Board game", "Board games"), ("Sport games", "Sport games"), 
    ("Sony Playstation", "Sony Playstation"), ("Watching film/anime", "Watching film/anime"), 
    ("Others", "Others")
)


MENU = ['Home', 'About', 'FAQ', 'Contact us', 'Rules']
USER_MENU =['Settings', 'Friends', 'Events','Chats']

class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE) 

def user_logged_in_handler(request, user, **kwargs):
    UserSession.objects.get_or_create(
        user = user,
        session_id = request.session.session_key
    )

def delete_user_sessions(user):
    user_sessions = UserSession.objects.filter(user = user)
    for user_session in user_sessions:
        user_session.session.delete()
