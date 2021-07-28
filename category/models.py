from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100,unique=True)
    slug = models.CharField(max_length=100,unique=True)
    description = models.TextField(blank=True)
    category_image = models.ImageField(upload_to = 'images/category')

    #Name appearing on the admin page, it was 'Categorys', we renamed it to 'Categories'
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        '''__str__ is the name that is stored on admin page '''
        return self.category_name
