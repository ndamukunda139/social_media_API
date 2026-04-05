from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# Register custom user model in admin


CustomUser = get_user_model()
@admin.register(CustomUser)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'bio']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'profile_picture')}),
    )
