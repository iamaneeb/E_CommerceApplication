from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.Home,name='home'),
    path('<slug:category_slug>/',views.Products,name='products'),
    path('<slug:product_slug>/',views.Productdetails,name='product_details')
    
]
