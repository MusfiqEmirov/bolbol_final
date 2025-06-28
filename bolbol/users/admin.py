from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models.user import User


class UserAdmin(BaseUserAdmin):
    # Fields to display in the user list
    list_display = ('id', 'phone_number', 'full_name', 'email', 'is_staff', 'is_active')
    list_display_links = ('id', 'full_name', 'phone_number')
    search_fields = ('full_name', 'phone_number', 'email')
    list_filter = ('is_staff', 'is_active', 'date_joined')

    # Sections in the user detail view
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'email')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields displayed during user creation
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'full_name', 'email', 'password1', 'password2'),
        }),
    )

    # Pagination and ordering
    ordering = ('-date_joined',)
    list_per_page = 25

admin.site.register(User, UserAdmin)