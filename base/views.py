from django.shortcuts import render, get_object_or_404, redirect
from .models import (
    Category,
    Product,
    Cart,
    CartItem,
    Account,
    Order,
    OrderProduct,
    Payment,
    ProductGallery,
)
from django.db.models import Q
from .form import RegistrationForm, OrderForm
from django.contrib import auth, messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import requests
import datetime

# email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def Register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            user.phone_number = phone_number
            user.save()
            # email registraction
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string(
                "base/account_verification_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.info(
                request,
                " Thank you for registering. A verification email has been sent to your inbox. Please check your email to activate your account.",
            )
            return redirect("register")
    else:
        form = RegistrationForm()
    context = {
        "form": form,
    }
    return render(request, "base/register.html", context)


def Login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    # if the cart is already there it should increse the quantity
                    cart_repeat_exist = CartItem.objects.filter(user=user)
                    if cart_repeat_exist:
                        for item in cart_repeat_exist:
                            item.quantity += 1
                            item.save()
                    # if the cart is not there
                    else:
                        for item in cart_item:
                            item.user = user
                            item.save()
            except:
                pass
            auth.login(request, user)
            # to get the url
            url = request.META.get("HTTP_REFERER")
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split("=") for x in query.split("&"))
                print(params)
                if "next" in params:
                    nextPage = params["next"]
                    return redirect(nextPage)
            except:
                return redirect("home")
        else:
            messages.error(request, "Invalid login credentials")
            return redirect("login")
    context = {}
    return render(request, "base/login.html", context)


def Logout(request):
    auth.logout(request)
    return redirect("home")


def Activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! Your account is activated.")
        return redirect("login")
    else:
        messages.error(request, "Invalid activation link")
        return redirect("register")


def ForgetPassword(request):
    if request.method == "POST":
        email = request.POST["email"]
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            mail_subject = "Reset Your Password"
            message = render_to_string(
                "base/forget_password_verification.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.info(
                request,
                "Password reset email has been send to your email address. Please check your inbox.",
            )
            return redirect("login")
        else:
            messages.error(request, "Account does not exist!")
            return redirect("forgetpassword")

    return render(request, "base/forget_password.html")


def Password_reset_verificaion(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.info(request, "Please reset your password")
        return redirect("resetpassword")
    else:
        messages.error(request, "This link has been expired!")
        return redirect("login")


def Resetpassword(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            uid = request.session.get("uid")
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.info(request, "Password reset successful")
            return redirect("login")
        else:
            messages.error(request, "Password do not match!")
            return redirect("resetpassword")
    else:
        return render(request, "base/resetpassword.html")


def Home(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "base/home.html", context)


def Products(request, category_slug=None):
    products = None
    categries = None
    if category_slug != None:
        categries = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categries)
    else:
        products = Product.objects.all()
    context = {
        "products": products,
    }
    return render(request, "base/products.html", context)


def Productdetails(request, product_slug, category_slug):
    pd = Product.objects.get(slug=product_slug)
    imagegallery = ProductGallery.objects.filter(product_id=pd.id)
    cart_prod = CartItem.objects.filter(
        cart__cart_id=_cart_id(request), product=pd
    ).exists()
    return render(
        request,
        "base/product-details.html",
        {
            "pd": pd,
            "cart_prod": cart_prod,
            "imagegalley" : imagegallery
        },
    )


######################################CART############################################
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    if current_user.is_authenticated:
        try:
            cart_item = CartItem.objects.get(product=product, user=current_user)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                user=current_user,
                quantity=1,
            )
            cart_item.save()
        return redirect("cart")
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=1,
            )
            cart_item.save()
        return redirect("cart")


def remove_cart(request, product_id):
    current_user = request.user
    if current_user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        cart_items = CartItem.objects.get(product=product, user=current_user)
        if cart_items.quantity > 1:
            cart_items.quantity -= 1
            cart_items.save()
        else:
            cart_items.delete()
        return redirect("cart")
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_items = CartItem.objects.get(product=product, cart=cart)
        if cart_items.quantity > 1:
            cart_items.quantity -= 1
            cart_items.save()
        else:
            cart_items.delete()
        return redirect("cart")


def delete_cart(request, product_id):
    current_user = request.user
    if current_user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        cart_items = CartItem.objects.get(product=product, user=current_user)
        cart_items.delete()
        return redirect("cart")
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_items = CartItem.objects.get(product=product, cart=cart)
        cart_items.delete()
        return redirect("cart")


def Cart_item(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.newprice * cart_item.quantity
            quantity += cart_item.quantity
    except Cart.DoesNotExist:
        pass
    except CartItem.DoesNotExist:
        pass

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
    }
    return render(request, "base/cart.html", context)


################################################################################


def Search(request):
    q = request.GET.get("q")  # Use .get() method to retrieve 'q' parameter

    if q:
        products = Product.objects.order_by("-created_date").filter(
            Q(brand__icontains=q)
            | Q(product_name__icontains=q)
            | Q(description__icontains=q)
            | Q(newprice__icontains=q)
        )
    else:
        products = Product.objects.order_by("-created_date")

    return render(
        request,
        "base/products.html",
        {
            "products": products,
        },
    )


def Store(request):
    products = Product.objects.order_by("-created_date")
    return render(request, "base/products.html", {"products": products})


@login_required(login_url="login")
def Checkout(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.newprice * cart_item.quantity
            quantity += cart_item.quantity
    except Cart.DoesNotExist:
        pass
    except CartItem.DoesNotExist:
        pass

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
    }
    return render(request, "base/checkout.html", context)

    ########## ORDER ####################


def Payment(request, total=0,quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    for cart_item in cart_items:
            total += cart_item.product.newprice * cart_item.quantity
            quantity += cart_item.quantity
    if 'order_data' in request.session:
        order_data = request.session['order_data']
        order_number = order_data.get('order_number')  # Get the total from the stored data 
    order = Order.objects.get(user=current_user,order_number=order_number,is_ordered=False)
    context={
                    "order":order,
                    "total":total,
                    "cart_items":cart_items,
                    "quantity": quantity,
                }
    return render(request, "base/payment.html",context)


def Place_order(request, total=0, quantity=0, cart_items=None):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect("store")
    else:
        for cart_item in cart_items:
            total += cart_item.product.newprice * cart_item.quantity
            quantity += cart_item.quantity

        if request.method == "POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                data = Order()
                data.user = current_user
                data.first_name = form.cleaned_data["first_name"]
                data.last_name = form.cleaned_data["last_name"]
                data.email = form.cleaned_data["email"]
                data.phone = form.cleaned_data["phone"]
                data.address_line_1 = form.cleaned_data["address_line_1"]
                data.address_line_2 = form.cleaned_data["address_line_2"]
                data.country = form.cleaned_data["country"]
                data.state = form.cleaned_data["state"]
                data.city = form.cleaned_data["city"]
                data.order_total = total
                data.ip = request.META.get("REMOTE_ADDR")
                data.save()

                yr = int(datetime.date.today().strftime("%Y"))
                dt = int(datetime.date.today().strftime("%d"))
                mt = int(datetime.date.today().strftime("%m"))
                d = datetime.date(yr, mt, dt)
                current_date = d.strftime("%Y%m%d")
                order_number = current_date + str(data.id)
                data.order_number = order_number
                data.save()
                # order = Order.objects.get(user=current_user,order_number=order_number,is_ordered=False)
                # context={
                #     "order":order,
                #     "total":total,
                #     "cart_items":cart_items,
                #     "quantity": quantity,
                # }
                request.session['order_data'] = {
                        'order_number': order_number,
    # Other relevant data you want to pass
                                }
                return redirect("payment")
            else:
                messages.error(request, "Fill the form")
                context = {
                    "total": total,
                    "quantity": quantity,
                    "cart_items": cart_items,
                }
                return render(request, "base/checkout.html", context)
        else:
            context = {
                    "total": total,
                    "quantity": quantity,
                    "cart_items": cart_items,
                }
            return render(request, "base/checkout.html",context)


def Profile(request):
    return render(request, "base/profile.html")