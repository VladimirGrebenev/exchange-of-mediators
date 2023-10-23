from django.contrib import admin

from .models import *


class ConflictAdmin(admin.ModelAdmin):
    list_display = (
        "created", "status", "creator", "mediator", "title", "country", "city")
    list_display_links = ("title",)
    search_fields = (
        "created", "status", "creator", "mediator", "title", "country", "city")
    list_editable = ("status",)
    list_filter = ("status", "country")
    list_per_page = 10


class ConflictResponseAdmin(admin.ModelAdmin):
    list_display = (
        "response_time", "conflict", "mediator", "rate", "time_for_conflict")
    list_display_links = ("response_time",)
    search_fields = (
        "mediator", "rate", "time_for_conflict")
    list_editable = ("rate",)
    list_filter = ("time_for_conflict",)
    list_per_page = 10


admin.site.register(Conflict, ConflictAdmin)
admin.site.register(Document)
admin.site.register(ConflictResponse, ConflictResponseAdmin)
