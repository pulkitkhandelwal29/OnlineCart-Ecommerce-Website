from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account
# Register your models here.

#There is field named 'password_validation' in models
#Django Admin does not show it as it is automatically taken
#We show using this and reading as readonly_fields so that no one can edit it
class AccountAdmin(UserAdmin):
    #shows these fields when we just open accounts section
    list_display = ('email','first_name','last_name','username','last_login','date_joined','is_active')
    #Make these fields clickable and then we can see more inside it
    list_display_links = ('email','first_name','last_name')
    #Making fields readonly
    readonly_fields = ('last_login','date_joined','password')
    #Ordering by date_joined (recent date joined people should come up)
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter  = ()
    fieldsets = ()  #Helps to keep password as read only as readonly field


admin.site.register(Account,AccountAdmin) #We need to pass the class made above to register in admin page
