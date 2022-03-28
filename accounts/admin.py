from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User, Region, Link, Language, EducationAndEmploymentHistory


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "phone", "region",
                                      "address", "profile", "place_of_birth", "skills",
                                      "hobbies", "languages", "achievements")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("username", "email", "first_name", "last_name", "phone", "region", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "region")
    list_select_related = ("region",)
    list_per_page = 10


admin.site.register(Region)
admin.site.register(Link)
admin.site.register(Language)
admin.site.register(EducationAndEmploymentHistory)
