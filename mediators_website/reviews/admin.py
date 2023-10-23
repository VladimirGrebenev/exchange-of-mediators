from django.contrib import admin

from .models import *


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("from_user", "to_user", "rating", "created_at")
    list_display_links = ("created_at",)
    search_fields = ("created_at", "from_user", "to_user")
    list_editable = ("rating",)
    list_filter = ("created_at",)
    list_per_page = 10


admin.site.register(Review, ReviewAdmin)
