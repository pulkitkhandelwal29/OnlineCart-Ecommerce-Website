from django.db import models

from django.urls import reverse

from category.models import Category

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    description = models.TextField(max_length=500,blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='images/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default = True)

    #Foreign key with Category and on_delete=models.cascade (if we delete category, products will also be deleted)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        '''Function bring url of the slug product'''
        return reverse('product_detail',args=[self.category.slug,self.slug]) #Passed two args :- category slug,product slug

    def __str__(self):
        return self.product_name

class VariationManager(models.Manager):
    '''It is there to classify color should go to color dropdown and size to size dropdown'''
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)

    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)

variation_category_choice = {
    ('color','color'),
    ('size','size'),
}

class Variation(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100,choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
