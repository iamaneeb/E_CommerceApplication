from django.shortcuts import render,get_object_or_404,redirect
from .models import Category,Product,Cart,CartItem,Account
from django.db.models import Q
from .form import RegistrationForm
from django.contrib import auth,messages

# Create your views here.
def Home(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, 'base/home.html', context)


def Products(request,category_slug=None):
    products = None
    categries = None
    if category_slug != None:
        categries = get_object_or_404(Category,slug = category_slug)
        products = Product.objects.filter(category=categries)
    else:    
        products = Product.objects.all()        
    context = {"products":products,}
    return render(request,'base/products.html',context)

def Productdetails(request,product_slug,category_slug):
    pd = Product.objects.get(slug=product_slug)
    cart_prod = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=pd).exists()
    return render(request,'base/product-details.html',{"pd":pd,"cart_prod":cart_prod,}) 

######################################CART############################################
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

    
    context = {
        'total' : total,
        'quantity':quantity,
        'cart_items':cart_items,
    }
    return render(request,'base/cart.html',context)

################################################################################

def Search(request):  
    q = request.GET.get('q')  # Use .get() method to retrieve 'q' parameter

    if q:
        products = Product.objects.order_by('-created_date').filter(Q(brand__icontains=q) | Q(product_name__icontains=q) | Q(description__icontains=q) | Q(newprice__icontains=q))
    else:
        products = Product.objects.order_by('-created_date')

    return render(request,'base/products.html',{'products':products,})

def Store(request):
    products = Product.objects.order_by('-created_date')
    return render(request,'base/products.html',{"products":products})

def Register(request):
    if request.method == "POST":
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name =form.cleaned_data['first_name']
            last_name =form.cleaned_data['last_name']    
            username =form.cleaned_data['username']    
            email =form.cleaned_data['email']    
            phone_number =form.cleaned_data['phone_number']    
            password =form.cleaned_data['password']    
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.phone_number=phone_number
            user.save()
            messages.success(request,"succeeeeddddd aneeb")
            return redirect('register')
    else:        
        form = RegistrationForm()
    context = {"form":form,}
    return render(request,'base/register.html',context)


def Login(request):  
    if request.method == "POST":
        email=request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Invalid login credentials")
            return redirect('login')
    context = {}
    return render(request,'base/login.html',context) 
