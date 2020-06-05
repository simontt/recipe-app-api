from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from .models import User, Tag, Ingredient


class UserAdmin(BaseUserAdmin):
    # Order by id, listing email and name
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        # Title for section None
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            # See Django admin docs
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Tag)
admin.site.register(Ingredient)
