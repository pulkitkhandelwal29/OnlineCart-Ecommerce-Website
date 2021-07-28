from django.contrib import admin

from .models import Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    #Making Prepopulated field meaning name entering in category_name automatically should appear in slug field
    prepopulated_fields = {'slug': ('category_name',)}
    #Appears at front page of categories
    list_display = ('category_name','slug')

admin.site.register(Category,CategoryAdmin)
