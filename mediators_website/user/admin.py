from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "firstname", "lastname", "email", "status", "is_active", "is_staff",
        "is_superuser", "deleted")
    list_display_links = ("firstname",)
    search_fields = ("status", "is_active", "is_staff", "deleted")
    list_editable = ("status", "is_active", "is_staff", "deleted")
    list_filter = ("status", "is_active", "is_staff", "deleted")
    list_per_page = 10


class BasicUserAdmin(admin.ModelAdmin):
    list_display = (
        "firstname", "lastname", "email", "status", "is_active", "is_staff",
        "is_superuser", "deleted")
    list_display_links = ("firstname",)
    search_fields = ("status", "is_active", "is_staff", "deleted")
    list_editable = ("status", "is_active", "is_staff", "deleted")
    list_filter = ("status", "is_active", "is_staff", "deleted")
    list_per_page = 10


class MediatorAdmin(admin.ModelAdmin):
    list_display = (
        "firstname", "lastname", "email", "status", "is_active", "is_staff",
        "is_superuser", "deleted")
    list_display_links = ("firstname",)
    search_fields = ("status", "is_active", "is_staff", "deleted")
    list_editable = ("status", "is_active", "is_staff", "deleted")
    list_filter = ("status", "is_active", "is_staff", "deleted")
    list_per_page = 10


admin.site.register(User, UserAdmin)
admin.site.register(EmailConfirmation)
admin.site.register(BasicUser, BasicUserAdmin)
admin.site.register(Mediator, MediatorAdmin)
admin.site.register(AdditionalInfo)
