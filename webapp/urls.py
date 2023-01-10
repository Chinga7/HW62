from django.urls import path
from webapp.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, add_to_cart, CartListView, OrderListView, CartDeleteView, OrderCreateView

app_name = 'webapp'

urlpatterns = [
    # Product urls
    path('', ProductListView.as_view(), name='product_list'),
    path('product/detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),

    # Cart urls
    path('cart/add/<int:pk>/<str:source>/',  add_to_cart, name='cart_add'),
    path('cart/list/',  CartListView.as_view(), name='cart_list'),
    path('cart/delete/<int:pk>/',  CartDeleteView.as_view(), name='cart_delete'),

    # Order urls
    path('order/list/', OrderListView.as_view(), name='order_list'),
    path('order/create/', OrderCreateView.as_view(), name='order_create'),

]
