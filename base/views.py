from django.shortcuts import render

# Create your views here.
def Home(request):
    return render(request,'base/home.html')

def Hoodies(request):
    return render(request,'base/hoodies.html')

def Productdetails(request):
    return render(request,'base/product-details.html')