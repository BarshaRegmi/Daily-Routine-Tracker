# app/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Import your custom user model
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    # Define fields to display in the admin list view
    list_display = ('email', 'name', 'profession', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'profession')
    search_fields = ('email', 'name')
    
    # Set ordering to avoid the username error
    ordering = ('email',)  # Order by email instead of username

    # Define fieldsets to avoid unknown fields like username, first_name, etc.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'photo', 'profession')}),
        (_('Permissions'), {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    # Adjust add_fieldsets for creating users without username, first_name, etc.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

# Register CustomUser with CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
