from django.contrib import admin

from goals.models import GoalCategory


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")
    readonly_fields = ("created", "updated", )
    list_filter = ("is_deleted", )


admin.site.register(GoalCategory, GoalCategoryAdmin)
