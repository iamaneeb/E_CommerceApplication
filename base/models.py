from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.urls import reverse

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError('User must have email address')
        
        if not username:
            raise ValueError('User must have an username')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self,first_name,last_name,username,email,password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin =True
        user.save(using=self._db)
        return user 


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=50)

    #required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    #if the user is admin he has all the permission to do the changes
    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,add_label):
        return True



class Category(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    cat_image = models.ImageField(upload_to='photos/categories',blank=True)

    class Meta:
        verbose_name = 'category'
        #the name you can see your admin site
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name
    


class Product(models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    oldprice = models.IntegerField()
    newprice = models.IntegerField()
    prod_img = models.ImageField(upload_to='photos/products')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    brand = models.CharField(default='COCAINJESUS',null=True,max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    availability = (('In Stock','In Stock'),('Out of Stock','Out of Stock'))
    description = models.TextField(null=True)
    feature = models.TextField(blank =True)
    is_available = models.CharField(choices=availability,null=True,max_length=100)

    def __str__(self):
        return self.product_name

    
    def get_url(self):
        return reverse('product_details',args=[self.category.slug,self.slug])


class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    

class CartItem(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE , null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.newprice * self.quantity
    
    def __str__(self):
        return self.product.product_name 


#########################ORDER#################################################

class Payment(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100) #total amount paid
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id
    

class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    )

    user = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100,unique=True)
    phone = models.CharField(max_length=50)
    address_line_1 =models.CharField(max_length=50)
    address_line_2 =models.CharField(max_length=50,blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_total = models.FloatField()
    status = models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True,max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.first_name
    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name


    
    


