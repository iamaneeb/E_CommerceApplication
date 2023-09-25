from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category,Account,Product,Cart,CartItem


class AccountAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','username','last_login','date_joined','is_active')
    list_display_links=('email','first_name','last_name')
    readonly_fields = ('last_login','date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class CategoryAdmin(admin.ModelAdmin):
    #its for to auto write the slug whatever typing in the category_name
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name','slug')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','newprice','category','created_date')
    prepopulated_fields = {'slug':('product_name',)}



# Register your models here.
admin.site.register(Category,CategoryAdmin)
admin.site.register(Account,AccountAdmin)
admin.site.register(Product,ProductAdmin) 
admin.site.register(Cart)
admin.site.register(CartItem)

