from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login,authenticate,logout
from .models import Product,Category,Cart,CartItem,Order,OrderItem
from .forms import OrderForm,ProductForm,CustomUserCreationForm,AuthenticationForm,CategoryForm
import logging
logger=logging.getLogger(__name__)


#@login_required
def product_list(request):
    products=Product.objects.filter(available=True)
    return render(request,'eshop/product_list.html',{'products': products})

def product_list_by_category(request,category_id):
    category=get_object_or_404(Category,id=category_id)
    products= category.products.filter(available=True)
    return render(request, 'eshop/product_list.html',{'category':category,'products':products})

def product_detail(request,id):
    product=get_object_or_404(Product , id=id,available=True)
    return render(request,'eshop/product_detail.html',{'product':product})

def add_product(request):
    if request.method == 'POST':
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'The product has been added successfully.')
            return redirect('product_list')
        else:
            messages.error(request, 'There are errors in the form. Please check again.')
    else:
        form=ProductForm()
    
    return render(request, 'eshop/add_product.html',{'form':form})            





def update_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ürün "{product.name}" başarıyla güncellendi.')
            return redirect('product_detail', id=product.id)
        else:
            messages.error(request, 'Formda hata var. Lütfen kontrol edin.')
    else:
        form = ProductForm(instance=product)
    return render(request, 'eshop/edit_product.html', {'form': form, 'product': product})






def product_delete(request,id):
    product=get_object_or_404(Product,id=id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return redirect('product_list')





def add_category(request):
    if request.method == 'POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Category added successfully.')
            return redirect('category_list')
    else:
        form=CategoryForm()
    
    return render(request,'eshop/add_category.html',{'form':form})




def category_list(request):
    categories=Category.objects.all()
    return render(request,'eshop/category_list.html',{'categories':categories})




def category_detail(request,id):
    category=get_object_or_404(Category,id=id)
    return render(request,'eshop/category_detail.html',{'category':category})




def edit_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Kategori "{category.name}" güncellendi.')
            return redirect('category_list_by_category', category_id=category.id)
    else:
        form = CategoryForm(instance=category)
    return render(request, 'eshop/edit_category.html', {'form': form, 'category': category})






def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Kategori silindi.')
        return redirect('category_list')
    return redirect('category_list')







def cart_detail(request):
    cart,created=Cart.objects.get_or_create(session_key=request.session.session_key)
    return render(request, 'eshop/cart_detail.html',{'cart':cart})

def cart_add(request,product_id):
    cart,created =Cart.objects.get_or_create(session_key=request.session.session_key)
    product=get_object_or_404(Product,id=product_id)
    cart_item,created=CartItem.objects.get_or_create(cart=cart,product=product)
    cart_item.save()
    messages.success(request,'The product has been added to the cart.')
    return redirect('cart_detail')

def cart_remove(request,product_id):
    cart=Cart.objects.get(session_key=request.session.session_key)
    product=get_object_or_404(Product,id=product_id)
    cart_item=get_object_or_404(CartItem,cart=cart,product=product)
    cart_item.delete()
    messages.success(request,'The product has been removed from the cart.')
    return redirect('cart_detail')

def cart_update(request):
    if request.method == 'POST':
        cart= Cart.objects.get(session_key=request.session.session_key)
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id=key.split('_')[1]
                quantity= int(value)
                product=get_object_or_404(Product, id=product_id)
                cart_item,created=CartItem.objects.get_or_create(cart=cart,product=product)
                cart_item.quantity=quantity
                cart_item.save()
                messages.success(request, f'Updated quantity for {product.name}')
        return redirect('cart_detail')
    return redirect('cart_detail')

def checkout(request):
    try:
        cart=Cart.objects.get(session_key=request.session.session_key)
    except Cart.DoesNotExist:
        messages.error(request,'Basket not found. Please add the product again.')
        return redirect('cart_detail')
    
    if request.method == 'POST':
        form =OrderForm(request.POST)
        if form.is_valid():
            order= form.save(commit=False)
            order.cart=cart
            order.paid_amount=sum(item.product.price * item.quantity for item in cart.items.all())
            order.save()
            
            #create OrderItems for each item in the cart
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
            
            messages.success(request,'Your order has been received successfully.')
            return redirect('orders_list')
        else:
            messages.error(request,'There are errors in the form. Please check again.')
    else:
        form=OrderForm()
    
    return render(request,'eshop/checkout.html',{'cart':cart,'form':form})

def orders_list(request):
    orders=Order.objects.prefetch_related('items__product').all()
    return render(request,'eshop/orders_list.html',{'orders':orders})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Account created for {username}!')
                return redirect('product_list')                                
    else:
        form = CustomUserCreationForm()  # only initialize here
    
    return render(request, 'eshop/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f'You are now logged in, {user.username}!')
            return redirect('product_list')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    
    return render(request, 'eshop/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request,'You have been logged out.')
    return redirect('product_list')                       