from django.db import models

from store.models import Product,Variation

from accounts.models import Account

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE, null=True) #made it so that all the cart items be transferred to logged in user
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    variations = models.ManyToManyField(Variation,blank=True) #Many products can have many variation
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE , null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self): #calculating sub_total in the cart page
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product
