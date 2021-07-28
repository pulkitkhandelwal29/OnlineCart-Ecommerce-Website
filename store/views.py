from django.shortcuts import render,get_object_or_404

from .models import Product

from category.models import Category
# Create your views here.

def home(request):
    products = Product.objects.all().filter(is_available=True)
    return render(request,'store/index.html',{'products':products})

def store(request,category_slug=None): #opening web page using slug (Store/shirts)
    #Display Products by Category
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug) #slug is what we defined in category models
        products = Product.objects.all().filter(category = categories,is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True) #For displaying products in store page
        product_count = products.count()        #count the total products for webpage

    return render(request,'store/store.html',{'products':products,'product_count':product_count})
    #method to pass information to html

def product_detail(request,category_slug,product_slug):
    ''' Product detail functionality'''
    try:
        #accessing slug of category(defined as foreign key) using __
        single_product = Product.objects.get(category__slug = category_slug, slug = product_slug )
    except Exception as e:
        raise e

    context = {'single_product':single_product} #Another way to pass information to html (creating dictionary before)
    return render(request,'store/product_detail.html',context)
