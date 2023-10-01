from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date_of_birth', 'is_deleted')
    list_filter = ('gender', 'nationality', 'is_deleted')
    actions = ['undelete_users']

    def undelete_users(self, request, queryset):
        queryset.update(is_deleted=False)
    undelete_users.short_description = 'Undelete selected users'