from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from PIL import Image

class Category(models.Model):
    name=models.CharField(max_length=100)
    description= models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name 

class Product(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name= models.CharField(max_length=100)
    image=models.ImageField(upload_to='products/',blank=True,null=True)
    description=models.TextField()
    price= models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField()
    available=models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img=Image.open(self.image.path)
            img=img.resize((300,300), Image.LANCZOS)
            img.save(self.image.path)
     
    def __str__(self):
        return self.name

class Cart(models.Model):
    session_key=models.CharField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.session_key
    
    def get_total_cost(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

class Order(models.Model):
    full_name=models.CharField(max_length=255)
    email=models.EmailField()
    address=models.CharField(max_length=255)
    paid=models.BooleanField(default=False)
    paid_amount=models.DecimalField(max_digits=10,decimal_places=2)
    created=models.DateTimeField(auto_now_add=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Order {self.id} by {self.full_name}'

class OrderItem(models.Model):
    order=models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    product=models.ForeignKey(Product,related_name='order_items',on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    
    def __str__(self):
        return f'Order Item {self.id}'   
    
class CustomUser(AbstractUser):
    bio=models.TextField(max_length=500,blank=True)
    location=models.CharField(max_length=30,blank=True)
    groups=models.ManyToManyField(Group,related_name='custom_user_set',blank=True)
    user_permissions = models.ManyToManyField(Permission,related_name='custom_user_set',blank=True)         
       