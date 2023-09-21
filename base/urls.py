from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.Home,name='home'),
    path('<slug:category_slug>/',views.Products,name='products'),
    path('<slug:category_slug>/<slug:product_slug>/',views.Productdetails,name='product_details'),
    path('cart', views.CartItem,name='cart'),

    
]
