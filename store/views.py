from django.shortcuts import render,get_object_or_404,redirect

from .models import Product , ReviewRating , ProductGallery

from category.models import Category

from carts.models import CartItem
from carts.views import _cart_id

#Paginator
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator

#Helps in quering and providing condition for OR (implemented in search)
from django.db.models import Q

from .forms import ReviewForm

from django.contrib import messages

from orders.models import OrderProduct
# Create your views here.

def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')

    #Get the reviews (for particular product, status also should be true- if admin doesn't want to show, he can disable status in admin page)
    for product in products:
        reviews = ReviewRating.objects.filter(product_id = product.id,status=True)

    return render(request,'store/index.html',{'products':products,'reviews':reviews})



def store(request,category_slug=None): #opening web page using slug (Store/shirts)
    #Display Products by Category
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug) #slug is what we defined in category models
        products = Product.objects.all().filter(category = categories,is_available=True).order_by('id')

        #Applying Paginator (providing paroducts,how much product you want to show)
        paginator = Paginator(products,3)
        #Accessing the below URL
        page = request.GET.get('page') #/store/shirts?page=2
        #We got 6 products in paged_products (need to passed to template as we just want to show 6 products)
        paged_products = paginator.get_page(page)

        product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True).order_by('id') #For displaying products in store page
        #Applying Paginator (providing paroducts,how much product you want to show)
        paginator = Paginator(products,6)
        #Accessing the below URL
        page = request.GET.get('page') #/store/shirts?page=2
        #We got 6 products in paged_products (need to passed to template as we just want to show 6 products)
        paged_products = paginator.get_page(page)

        product_count = products.count()        #count the total products for webpage

    context = {
    'products': paged_products,
    'product_count': product_count,
    }
    return render(request,'store/store.html',context)
    #method to pass information to html




def product_detail(request,category_slug,product_slug):
    ''' Product detail functionality'''
    try:
        #accessing slug of category(defined as foreign key) using __
        single_product = Product.objects.get(category__slug = category_slug, slug = product_slug )
        #checking if product exist in cart (using filter)--returns true or false
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e

    #checking if user has bought the product, then only he will be able to review
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user = request.user,product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct=None

    else:
        orderproduct=None

    #Get the reviews (for particular product, status also should be true- if admin doesn't want to show, he can disable status in admin page)
    reviews = ReviewRating.objects.filter(product_id = single_product.id,status=True)

    #Get the product gallery images
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {  #Another way to pass information to html (creating dictionary before)
    'single_product':single_product,
    'in_cart':in_cart,
    'orderproduct':orderproduct,
    'reviews':reviews,
    'product_gallery':product_gallery
    }
    return render(request,'store/product_detail.html',context)




def search(request):
    '''Search functionality'''
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            #will look into the description and product_name of product and search for keyword
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains = keyword))
            product_count = products.count()
    context = {'products':products,'product_count':product_count}
    return render(request,'store/store.html',context)



def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER') #store the page of URL
    if request.method == "POST":
        try:
            #if reviews exist for the user, update the reviews
            reviews = ReviewRating.objects.get(user__id = request.user.id,product__id = product_id) #fetching the id from user (foreign key)
            form = ReviewForm(request.POST, instance = reviews) #we want to check if already reviews by user, update the review
            form.save()
            messages.success(request,'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            #if no reviews exist, create a new one
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request,'Thank you! Your review has been submitted.')
                return redirect(url)
