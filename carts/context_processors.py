from .models import Cart,CartItem

from .views import _cart_id

def counter(request):
    '''Count no. of items in cart (for showing dynamic counter in cart sign)'''
    cart_count=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id = _cart_id(request))
            cart_items = CartItem.objects.all().filter(cart = cart[:1]) #we want only 1 result
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count=0
    return dict(cart_count=cart_count)
