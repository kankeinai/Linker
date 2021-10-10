from django import forms
from django.forms import widgets
from .models import Profile, Event
from django.contrib.auth.models import User
from django.utils import timezone
from .utilities import INTERESTS

class RegisterForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs = {'placeholder':'Username','class':'form-input',}))
    first_name = forms.CharField(widget=forms.TextInput(attrs = {'placeholder':'First name','class':'form-input',}))
    last_name = forms.CharField(widget=forms.TextInput(attrs = {'placeholder':'Last name','class':'form-input',}))
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs = {'placeholder':'E-mail','class':'form-input',}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs = {'placeholder':'Password','class':'form-input',}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs = {'placeholder':'Password repeat','class':'form-input',}))

    def is_valid(self):
        valid = super(RegisterForm, self).is_valid()
        if User.objects.filter(username = self.cleaned_data.get('username')).first():
            self.add_error("username", u"This username is already taken")
            return False
        if User.objects.filter(username = self.cleaned_data.get('email')).first():
            self.add_error("email", u"This email is already taken")
            return False
        if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            self.add_error("password_confirm", u"Пароли не совпадают")
            return False

        return valid
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'balance', 'friends', 'is_active', 'avatar_mini', 'avatar_date']
        
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['slug', 'author','luxe','published']
        

 
class SearchForm(forms.Form):
    date = forms.DateTimeField(required=False, initial=timezone.now().date,  widget=forms.DateTimeInput(attrs = {'placeholder':'When?','class':'search-input',}))
    category = forms.ChoiceField(required=False, choices=INTERESTS)
    from_p = forms.IntegerField(required=False, widget=forms.NumberInput(attrs = {'placeholder':'Min','class':'search-input','min':1,'max':20}))
    to_p = forms.IntegerField(required=False, widget=forms.NumberInput(attrs = {'placeholder':'Max','class':'search-input','min':1,'max':20}))
    search = forms.CharField(required=False, widget=forms.TextInput(attrs = {'placeholder':'I will find everything...or no','class':'search-input search'}))

 
    
