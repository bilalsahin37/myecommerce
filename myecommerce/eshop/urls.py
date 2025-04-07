from django.urls import path
from .views import product_list,product_list_by_category,product_detail,product_delete
from .views import cart_detail,cart_add,cart_remove,cart_update,checkout
from .views import register,login_view,logout_view,orders_list,add_product,add_category, category_list,edit_category,delete_category, category_detail

urlpatterns = [
    
    path('',product_list,name='product_list'),
    path('add-product/',add_product,name='add_product'),
    path('product/<int:id>/',product_detail,name='product_detail'),
    path('product/delete/<int:id>/',product_delete,name='product_delete'),



    
    path('register/',register,name='register'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
   



    path('category/<int:category_id>/',product_list_by_category,name='product_list_by_category'),
    path('add-category/',add_category,name='add_category'),
    path('categories/<int:id>/', category_detail, name='category_detail'),
    path('categories/', category_list, name='category_list'),
    path('category/edit/<int:category_id>/', edit_category, name='edit_category'),
    path('category/delete/<int:category_id>/', delete_category, name='delete_category'),


    
    path('cart/add/<int:product_id>/',cart_add,name='cart_add'),
    path('cart/remove/<int:product_id>/',cart_remove,name='cart_remove'),
    path('cart/update/',cart_update,name='cart_update'),
    path('cart/',cart_detail,name='cart_detail'),
    path('checkout/',checkout,name='checkout'),
    path('orders/',orders_list,name='orders_list'),
]
