from django.shortcuts import render,get_object_or_404
from .models import Category,Product


# Create your views here.
def Home(request):
    categories = Category.objects.all()
    context = {"categories":categories}
    return render(request,'base/home.html',context)

def Products(request,category_slug=None):
    products = None
    categries = None
    if category_slug != None:
        categries = get_object_or_404(Category,slug = category_slug)
        products = Product.objects.filter(category=categries)
    else:    
        products = Product.objects.all()
    context = {"products":products}
    return render(request,'base/products.html',context)

def Productdetails(request,product_slug):
    return render(request,'base/product-details.html',{})