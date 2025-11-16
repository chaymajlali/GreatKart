from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
from django.utils.html import format_html

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name','username', 'last_login', 'date_joined',  'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login') #lecture seule
    ordering = ('-date_joined',)#ordre decroissant

    filter_horizontal = ()
    list_filter = ()
    #mdps et lecture seule
    fieldsets = ()


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.profile_picture and hasattr(object.profile_picture, 'url'):
            return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
        else:
            return format_html('<img src="/static/images/default-avatar.png" width="30" style="border-radius:50%;">')
    thumbnail.short_description = 'Profile Picture'

    list_display = ('thumbnail', 'user', 'city', 'state', 'country')



admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)