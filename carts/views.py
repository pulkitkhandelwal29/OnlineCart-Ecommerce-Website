from django.shortcuts import render,redirect,get_object_or_404

from store.models import Product,Variation

from .models import Cart,CartItem

from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse

from django.contrib.auth.decorators import login_required


# Create your views here.
def cart(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated: #displaying the cart for logged in user
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request)) #Accessing cart using cart_id
            cart_items = CartItem.objects.filter(cart=cart,is_active=True) #Filtering cart_items based on cart
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100
        grand_total = total + tax

    except ObjectDoesNotExist: #if cart has 0 items, no error will be shown
        pass #ignore, if object does not exist

    #total cart_items, total price,quantity added,tax,grand_total
    context = {'total':total,'quantity':quantity,'cart_items':cart_items,'tax':tax,'grand_total':grand_total}
    return render(request,'carts/cart.html',context)


def _cart_id(request):
    '''Creates Cart Id using Session Id so that we can fetch '''
    cart = request.session.session_key #grab session key
    if not cart:
        cart = request.session.create() #if no cart is there, create a session key

    return cart




def add_cart(request,product_id):
    '''Adds product in cart when clicked on "Add to Cart"'''

    current_user = request.user
    product = Product.objects.get(id = product_id) #This will get the product (needed in add cart, variation thing)

    #if the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method =='POST':
            #Product variation /store/shirt/?color=red&size=large
            # color = request.POST['color']
            # size = request.POST['size']
            #Making it smarter to detect whether it is color,size,brand,author etc.
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        ### Grouping cart item variations
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user) #Combined product and cart to get cart item
            # existing_variations -> database
            # current variation -> product_variation
            # item_id -> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                #create a new cart item
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation) #Product variation in cart Cart Items
                item.save()   #Save cart_item information

        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')

    #if the user is not authenticated
    else:
        product_variation = []
        if request.method =='POST':
            #Product variation /store/shirt/?color=red&size=large
            # color = request.POST['color']
            # size = request.POST['size']
            #Making it smarter to detect whether it is color,size,brand,author etc.
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) #Get the cart usin cart id present in the session
        except Cart.DoesNotExist:
            #create a new cart
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()   #save the cart

        ### Grouping cart item variations
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart) #Combined product and cart to get cart item
            # existing_variations -> database
            # current variation -> product_variation
            # item_id -> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                #create a new cart item
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation) #Product variation in cart Cart Items
                item.save()   #Save cart_item information

        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')





def remove_cart(request,product_id,cart_item_id):
    ''' Decrement Product quantity by 1 and if less than 1, item will be deleted'''
    product = get_object_or_404(Product,id = product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product,user=request.user,id=cart_item_id)

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product,cart=cart,id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    except:
        pass

    return redirect('cart')



def remove_cart_item(request,product_id,cart_item_id):
    ''' When clicked on remove, item will be removed'''

    product = get_object_or_404(Product,id = product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
    #delete product from cart when clicked on remove
    cart_item.delete()

    return redirect('cart')



@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated: #displaying the cart for logged in user
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request)) #Accessing cart using cart_id
            cart_items = CartItem.objects.filter(cart=cart,is_active=True) #Filtering cart_items based on cart
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100
        grand_total = total + tax

    except ObjectDoesNotExist: #if cart has 0 items, no error will be shown
        pass #ignore, if object does not exist

    #total cart_items, total price,quantity added,tax,grand_total
    context = {
    'total':total,
    'quantity':quantity,
    'cart_items':cart_items,
    'tax':tax,
    'grand_total':grand_total
    }

    return render(request,'carts/checkout.html',context)
