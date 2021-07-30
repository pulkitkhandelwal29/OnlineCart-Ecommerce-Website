from django.shortcuts import render,redirect,get_object_or_404

from store.models import Product,Variation

from .models import Cart,CartItem

from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def cart(request,total=0,quantity=0,cart_items=None):
    try:
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

    product = Product.objects.get(id = product_id) #This will get the product (needed in add cart, variation thing)

    product_variation = []
    if request.method=='POST':
        #Product variation /store/shirt/?color=red&size=large
        # color = request.POST['color']
        # size = request.POST['size']
        #Making it smarter to detect whether it is color,size,brand,author etc.
        for item in request.POST:
            key=item
            value = request.POST[key]

            try:
                #iexact is exact matching
                variation = Variation.objects.get(product = product ,variation_category__iexact=key,varition_value__iexact=value)
                product_variation.append(variation)
            except:
                pass

    try:
        cart = Cart.objects.get(cart_id = _cart_id(request)) #Get the cart usin cart id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(    #create a new cart
        cart_id = _cart_id(request)
        )
    cart.save()   #save the cart

    try:
        cart_item = CartItem.objects.get(product = product,cart=cart) #Combined product and cart to get cart item

        #Product variation in cart Cart Items
        if len(product_variation) > 0:
            for item in product_variation: # it will iterate over that list and select the item
                cart_item.variation.add(item)

        cart_item.quantity += 1  #Cart quantity to be incremented by 1
        cart_item.save()   #Save cart_item information
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(  #If no cart_item, create new one
            product = product,
            quantity = 1,
            cart = cart,
        )
        #Product variation in cart Cart Items
        if len(product_variation) > 0:
            for item in product_variation:
                cart_item.variation.add(item)
        cart_item.save()
    return redirect('cart')





def remove_cart(request,product_id):
    ''' Decrement Product quantity by 1 and if less than 1, item will be deleted'''
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product,id = product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')



def remove_cart_item(request,product_id):
    ''' When clicked on remove, item will be removed'''
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product,id = product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    #delete product from cart when clicked on remove
    cart_item.delete()

    return redirect('cart')
