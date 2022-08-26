from django.contrib import admin

# Register your models here.
from bot.models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'username', 'user')
    readonly_fields = ('verification_code', )
