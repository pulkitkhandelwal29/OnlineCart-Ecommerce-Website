from django.contrib import admin

from .models import Product,Variation,ReviewRating,ProductGallery

#pip install django-admin-thumbnails (used for displaying image thumbnails in admin page)
import admin_thumbnails
# Register your models here.

@admin_thumbnails.thumbnail('image') #image is the field in Product Gallery (models)
class ProductGalleryInline(admin.TabularInline):
    '''Showing product gallery photos in Product admin page'''
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','modified_date','is_available')
    prepopulated_fields = {'slug':('product_name',)} #Prepopulating fields like slug

    inlines = [ProductGalleryInline] #displaying product gallery photos in Product admin page (using TabularInline)


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    #it provides a check box on the value in django admin front page
    list_editable = ('is_active',)
    #filtering on the basis of these (right hand side pane appears)
    list_filter = ('product','variation_category','variation_value')


admin.site.register(Product,ProductAdmin)

admin.site.register(Variation,VariationAdmin)

admin.site.register(ReviewRating)

admin.site.register(ProductGallery)
