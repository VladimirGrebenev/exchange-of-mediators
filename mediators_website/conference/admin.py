from django.contrib import admin

from .models import *


class ConferencesAdmin(admin.ModelAdmin):
    list_display = ("created_at", "initiator", "scheduled_date")
    list_editable = ("scheduled_date",)
    list_display_links = ("initiator",)
    list_per_page = 10


admin.site.register(Conferences, ConferencesAdmin)
