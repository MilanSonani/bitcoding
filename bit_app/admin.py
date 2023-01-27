from django.contrib import admin

from .models import CustomUser, Calendar
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'date_of_birth', 'primary_contact_number', 'currency']


class CalendarAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'start_time', 'end_time', 'recurrence']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Calendar, CalendarAdmin)
