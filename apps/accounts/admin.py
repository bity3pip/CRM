from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'role', 'is_online', 'last_seen', 'is_staff']
    list_filter = ['role', 'is_online']
    fieldsets = UserAdmin.fieldsets + (
        ('CRM', {'fields': ('role', 'is_online', 'last_seen')}),
    )
