from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .utilities import INTERESTS
from django.urls import reverse
from django.conf import settings
from PIL import Image
from django.utils import timezone



GENDER_CHOICES = [
    ['male', u"Male"],
    ['female', u"Female"],
    ['other', u"Not binary"]
]
from django.core.files import File
import os
from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=u"User")
    
    avatar = models.ImageField(verbose_name=u"Avatar", default="user.png" , null=True, blank=True)
    avatar_mini = models.ImageField(verbose_name=u"Avatar_mini", default="user.png" , null=True, blank=True)
    avatar_date = models.DateField(null=True, blank=True, verbose_name=u"Image date")
    
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name=u"About")
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name=u"City")
    birth_date = models.DateField(null=True, blank=True, verbose_name=u"Birth date")
    balance = models.PositiveIntegerField( default=0, verbose_name=u"Balance")
    gender = models.CharField(max_length=10, verbose_name=u"Gender", choices=GENDER_CHOICES, default="male")
    friends = models.ManyToManyField('self', blank=True)
    is_active = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        super().save()
        if self.avatar:
            img = Image.open(self.avatar)
            img = img.convert('RGB')
            new_name = self.user.username+".jpg"
            img.save(settings.MEDIA_ROOT+"/"+new_name, quality=75)
            os.remove(self.avatar.path) 
            self.avatar = new_name 
            self.avatar_mini = self.cropper(self.user.username, self.avatar.path)
            
            self.avatar_date = timezone.now().date()
            super().save()
        
    def cropper(self, username, img):
        img = Image.open(img)
        width, height = img.size  # Get dimensions
        if width > 600 and height > 600:
            # keep ratio but shrink down
            img.thumbnail((width, height))
            # check which one is smaller
        if height < width:
            # make square by cutting off equal amounts left and right
            left = (width - height) / 2
            right = (width + height) / 2
            top = 0
            bottom = height
            img = img.crop((left, top, right, bottom))

        elif width < height:
            # make square by cutting off bottom
            left = 0
            right = width
            top = 0
            bottom = width
            img = img.crop((left, top, right, bottom))

        if width > 600 and height > 600:
            img.thumbnail((600, 600))
            
        new_name = username+"-mini.jpg"
        img.save(settings.MEDIA_ROOT+"/"+ new_name)      
        
        return new_name
        
    
class Event(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique_for_date="date_time")
    tags = models.CharField(max_length=150, default='event')
    author = models.ForeignKey(User, on_delete=models.CASCADE, )
    short_desc = models.TextField(max_length=200)
    details = models.TextField(max_length=500)
    date_time = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=50, choices=INTERESTS[1:], default="Board games")
    num_people = models.PositiveSmallIntegerField(default = 1)
    published = models.BooleanField(default=True)
    luxe = models.BooleanField(default=False)
    
    def save(self, *args, **kw):
        ## your custom date logic to verify if expired or not.
        if self.date_time < timezone.now():
            self.published = False
        super(Event, self).save(*args, **kw)
    
    def prev_post(self):
        events = Event.objects.filter(published=True).order_by('date-time')
        for event in events:
            if event.published_date < self.published_date:
                return event.pk
        return event.pk

    def prev_post(self):
        events = Event.objects.filter(published=True).order_by('date-time')
        for event in events:
            if event.published_date > self.published_date:
                return event.pk
        return event.pk
    
        
    def get_absolute_url(self):
        return reverse('post_detail',
                        args=[self.date_time.year, User.username,
                              self.slug])
    class Meta:
        ordering = ('date_time',)

    def __str__(self):
        return self.title
    
    
        
