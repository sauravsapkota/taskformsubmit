from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date_of_birth', 'is_deleted')
    list_filter = ('gender', 'nationality', 'is_deleted')
    actions = ['mark_as_deleted', 'undelete_users']

    def mark_as_deleted(self, request, queryset):
        for user in queryset:
            user.mark_as_deleted()
    mark_as_deleted.short_description = 'Soft delete selected users'

    def undelete_users(self, request, queryset):
        for user in queryset:
            user.undelete_users()
    undelete_users.short_description = 'Undelete selected users'
