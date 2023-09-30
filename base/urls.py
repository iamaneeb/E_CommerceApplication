from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.Home,name='home'),
    path('<slug:category_slug>/',views.Products,name='products'),
    path('<slug:category_slug>/<slug:product_slug>/',views.Productdetails,name='product_details'),
    path('cart', views.Cart_item,name='cart'),
    path('add_cart/<int:product_id>', views.add_cart,name='add-cart'),
    path('remove_cart/<int:product_id>', views.remove_cart,name='remove-cart'),
    path('delete_cart/<int:product_id>', views.delete_cart,name='delete-cart'),




    
]
