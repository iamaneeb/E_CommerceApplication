from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category,Account,Product,Cart,CartItem,Payment,Order,OrderProduct,ProductGallery
import admin_thumbnails



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
#admin thumbnail package allow you to see the image in your db
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    #you can add extra image 
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','newprice','category','created_date')
    prepopulated_fields = {'slug':('product_name',)}
    #to see the productgallery in product 
    inlines = [ProductGalleryInline]



# Register your models here.
admin.site.register(Category,CategoryAdmin)
admin.site.register(Account,AccountAdmin)
admin.site.register(Product,ProductAdmin) 
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(ProductGallery)



