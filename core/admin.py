from django.contrib import admin

from .models import User

# admin.site.register(User)
@admin.register(User)
class BoardAdmin(admin.ModelAdmin):
    exclude = ("password",)
    readonly_fields = ("date_joined", "last_login", )
    list_display = ("username", "email", "first_name", "last_name", )
    list_filter = ("is_staff", "is_active", "is_superuser", )
    search_fields = ("username", "email", "first_name", "last_name", )