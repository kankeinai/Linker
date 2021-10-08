from django.contrib import admin
from .models import Event, Profile

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'date_time', 'published')
    list_filter = ('published', 'date_time', 'author')
    search_fields = ('title', 'tags', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date_time'
    ordering = ['published', 'date_time']
    
admin.site.register(Event, EventAdmin)
admin.site.register(Profile)
# Register your models here.
