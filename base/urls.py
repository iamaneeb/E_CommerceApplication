from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.Home,name='home'),
    path('search',views.Search,name='search'),
    path('<slug:category_slug>/',views.Products,name='products'),
    path('store',views.Store,name="store"),
    path('<slug:category_slug>/<slug:product_slug>/',views.Productdetails,name='product_details'),
    path('cart', views.Cart_item,name='cart'),
    path('add_cart/<int:product_id>', views.add_cart,name='add-cart'),
    path('remove_cart/<int:product_id>', views.remove_cart,name='remove-cart'),
    path('delete_cart/<int:product_id>', views.delete_cart,name='delete-cart'),
    path('register',views.Register,name="register"),
    path('login',views.Login,name="login"),
    path('logout',views.Logout,name='logout'),
    path('activate/<uidb64>/<token>/',views.Activate,name='activate'),
    path('forgetpassword',views.ForgetPassword,name="forgetpassword"),
    path('password_reset_confirm/<uidb64>/<token>/',views.Password_reset_verificaion,name="password_reset_confirm"),
    path('resetpassword',views.Resetpassword,name="resetpassword"),



    
]
