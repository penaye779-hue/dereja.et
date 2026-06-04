from django.contrib import admin
from .models import Application

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'job__title')

admin.site.register(Application, ApplicationAdmin)