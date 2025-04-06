from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Product,Category,Cart,CartItem,Order,CustomUser
from .forms import CustomUserCreationForm,CustomUserChangeForm

class ProductAdmin(admin.ModelAdmin):
    list_display=('name','category','price','stock','available')
    list_filter=('available','category')
    search_fields=('name','category__name')
    
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','description')
    search_fields=('name',)

class CartItemInline(admin.TabularInline):
    model=CartItem
    extra=0

class CartAdmin(admin.ModelAdmin):
    list_display=('id','session_key','created','updated')
    search_fields=('session_key',)
    inlines= [CartItemInline]
    
class OrderAdmin(admin.ModelAdmin):
    list_display=('id','full_name','email','paid','created')
    list_filter=('paid','created')
    search_fields=('full_name','email')
    readonly_fields=('cart','paid_amount')

class CustomUserAdmin(BaseUserAdmin):
    form=CustomUserChangeForm
    add_form=CustomUserCreationForm
    
    fieldsets=(
        (None,{'fields':('username','password')}),
        ('Personel info',{'fields':('first_name','last_name','email','bio','location')}),
        ('Permissions ',{'fields':('is_active','is_staff','is_superuser')}),
        ('Important dates ',{'fields':('last_login','date_joined',)}),
    )
    
    add_fieldsets=(
        (None,{
            'classes':('wide',),
            'fields':('username','email','password1','password2','bio','location'),
        })
    )
    list_display=('username','email','bio','location','is_staff')
    search_fields=('username','email','bio','location')
    ordering=('username',)

admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(CustomUser,CustomUserAdmin)                    