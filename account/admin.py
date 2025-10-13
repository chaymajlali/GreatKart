from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
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
admin.site.register(Account, AccountAdmin)