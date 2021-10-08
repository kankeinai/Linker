from django.shortcuts import render, get_object_or_404, redirect
from .models import Event
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utilities import MENU, user_logged_in_handler, delete_user_sessions
from django.contrib.auth import views as auth_views
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth import logout, login
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.views.generic.base import TemplateView, View
from .forms import RegisterForm
from django.urls import reverse
from .models import Profile
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, EventForm, SearchForm
from django.utils import timezone
from django.contrib.sessions.models import Session


class RegisterView(TemplateView):
    template_name = "registration/registration.html"
    def dispatch(self, request, *args, **kwargs):
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                self.create_new_user(form)
                return redirect(reverse("login"))
        context = {
            'form': form,
            'menu': MENU,
        }
        return render(request, self.template_name, context)

    def create_new_user(self, form):
        email = None
        if 'email' in form.cleaned_data:
            email = form.cleaned_data['email']
        
        User.objects.create_user(form.cleaned_data['username'], email, form.cleaned_data['password'],
                                 first_name=form.cleaned_data['first_name'],
                                 last_name=form.cleaned_data['last_name'])

class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        
        request.user.profile.is_active = False

        logout(request)
        return redirect("/accounts/login")
    
    

class ProfileView(TemplateView):
    template_name = "registration/profile.html"   
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("login"))
                            
        if not Profile.objects.filter(user=request.user).exists():
            return redirect(reverse("edit_profile"))
        
        user = request.user
        request.user.profile.is_active = True
        
        user_profile = Profile.objects.get(user = user)
        form = EventForm()
        
        
        
        try:
            user = User.objects.filter(username=request.GET.get('user'))[0]
        except:
            print('Error opening profile')
        
        events = Event.objects.filter(published=True, author=user, date_time__gt=timezone.now()).order_by('date_time')
        
        friend_list = Profile.objects.get(user = user).friends.all()
        
        if request.user!=user:
            friend_list.exclude(user = request.user)[:10]
            
        list = [item.user for item in friend_list]
        context = {
            'selected_user': user,
            'menu': MENU,
            'events': events,
            'form': form,
            'list': list
        }
        context['friend'] = user_profile.friends.filter(pk = user.profile.pk).exists()
        print(context['friend'])  
    
        op = request.GET.get('friend')
        if op=="add":
            user_profile.friends.add(user.profile.id)
            context['friend']=True
            print(context['friend'])
        elif op=="delete":
            user_profile.friends.remove(user.profile.id)
            context['friend']=False
            print(context['friend'])
        if request.method == 'POST':
            form = EventForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect(reverse("profile"))
        return render(request, self.template_name, context)     


    


class EditProfileView(TemplateView):
    template_name = "registration/edit_profile.html"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("login"))
        
        form = ProfileForm(instance=self.get_profile(request.user))
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=self.get_profile(request.user))
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                return redirect(reverse("profile"))
      
        return render(request, self.template_name, {'form': form, 'menu': MENU})

    def get_profile(self, user):
        try:
            return user.profile
        except:
            return None

class PostView(TemplateView):
    template_name = "home.html"
    def dispatch(self, request, *args, **kwargs):
        now = timezone.now()
        events = Event.objects.filter(published=True, date_time__gt= now).order_by('date_time')
        people = User.objects.exclude(id=request.user.id).order_by('-id')[:6]
        form =  SearchForm()
        
        if request.method=="GET":
            form = SearchForm(request.GET)
            if form.is_valid():
                q = request.GET.get("search")
                category = request.GET.get("category")
                from_p = request.GET.get("from_p")
                to_p = request.GET.get("to_p")
                date = request.GET.get("date")
        
                if q:
                    events = events.filter(tags__contains = q) 
                if category!='all' and category:
                    events = events.filter(category = category)
                if not from_p:
                    from_p = 1
                if not to_p:
                    to_p = 20
                events = events.filter(num_people__range=[from_p, to_p])
                if date:
                    events = events.filter(date_time__date = date)
            
        count = len(events)
        paginator = Paginator(events, 9)  # 3 posts in each page
        page = request.GET.get('page')
        try:
            events = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            events = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            events = paginator.page(paginator.num_pages)
        return render(request, 'home.html', {'page': page,
                                            'events': events,
                                            'menu': MENU,
                                            'form': form,
                                            'counter':count,
                                            'people':people})

        
    
def send_page(request):
    return render(request, 'home.html', {'menu': MENU})

