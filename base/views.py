from django.shortcuts import render,get_object_or_404,redirect
from .models import Category,Product,Cart,CartItem


# Create your views here.
def Home(request):
    categories = Category.objects.all()
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    cart_length = cart_items.count()
    context = {"categories":categories,"len":cart_length}
    return render(request,'base/home.html',context)

def Products(request,category_slug=None):
    products = None
    categries = None
    if category_slug != None:
        categries = get_object_or_404(Category,slug = category_slug)
        products = Product.objects.filter(category=categries)
    else:    
        products = Product.objects.all()
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    cart_length = cart_items.count()    
    context = {"products":products,"len":cart_length}
    return render(request,'base/products.html',context)

def Productdetails(request,product_slug,category_slug):
    pd = Product.objects.get(slug=product_slug)
    cart_prod = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=pd).exists()
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    cart_length = cart_items.count()
    return render(request,'base/product-details.html',{"pd":pd,"cart_prod":cart_prod,"len":cart_length}) 


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart    

def add_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))    
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            cart = cart,
            quantity = 1,
        )
        cart_item.save()
    return redirect('cart')

def remove_cart(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_items = CartItem.objects.get(product=product,cart=cart)
    if cart_items.quantity > 1:
        cart_items.quantity -= 1
        cart_items.save()
    else:
        cart_items.delete()
    return redirect('cart')    

def delete_cart(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_items = CartItem.objects.get(product=product,cart=cart)
    cart_items.delete()
    return redirect('cart')


def Cart_item(request,total=0,quantity=0,cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.newprice * cart_item.quantity)  
            quantity += cart_item.quantity
    except Cart.DoesNotExist:
        pass          
    except CartItem.DoesNotExist:
        pass
    cart_length = cart_items.count()
    print(cart_length)
    context = {
        'total' : total,
        'quantity':quantity,
        'cart_items':cart_items,
        'len' :cart_length
    }
    return render(request,'base/cart.html',context)