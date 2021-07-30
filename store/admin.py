from django.contrib import admin

from .models import Product,Variation
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','modified_date','is_available')
    prepopulated_fields = {'slug':('product_name',)} #Prepopulating fields like slug


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    #it provides a check box on the value in django admin front page
    list_editable = ('is_active',)
    #filtering on the basis of these (right hand side pane appears)
    list_filter = ('product','variation_category','variation_value')



admin.site.register(Product,ProductAdmin)

admin.site.register(Variation,VariationAdmin)
