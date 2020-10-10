from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from apps.users.models import User


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'token')
    fieldsets = [(None, {'fields': list_display + ('password',)})]
    readonly_fields = ('token',)
