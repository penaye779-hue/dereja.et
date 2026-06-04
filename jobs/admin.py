from django.contrib import admin
from .models import Job
from .models import Job, Category
from .models import ContactMessage
from django import forms
from .models import Subscriber
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location',  'created_at' )
    list_filter = ('location', 'created_at')
    search_fields = ('title', 'description')

admin.site.register(Job, JobAdmin)
admin.site.register(Category)
admin.site.register(Subscriber)
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']