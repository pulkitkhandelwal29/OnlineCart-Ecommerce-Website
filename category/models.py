from django.db import models

from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.TextField(blank=True)
    category_image = models.ImageField(upload_to = 'images/category')

    #Name appearing on the admin page, it was 'Categorys', we renamed it to 'Categories'
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        '''Function bring url of the slug category'''
        #products_by_category is in urls of store
        return reverse('products_by_category',args =[self.slug])

    def __str__(self):
        '''__str__ is the name that is stored on admin page '''
        return self.category_name
