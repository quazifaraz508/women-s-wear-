from django.urls import path
from . import views
from addToCart import views as ad_vs

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name="product_detail"),
    path('<int:prod_id>/delete/', views.product_delete, name='product_delete'),
    path('toggle-favorite/', views.toggle_fav, name='toggle_favorite'),
    path('favorites/', views.favorite_products_view, name='favorite_products'),
    path('contact/', views.contact, name='contact'),
    path('collections/', views.collections, name='collections'),
    path('add-to-cart/<int:product_id>/', ad_vs.add_to_cart, name='add_to_cart'),
    path('cart/', ad_vs.cart_summary, name='cart_summary'),
    path('cart/dropdown/', ad_vs.cart_dropdown, name='cart_dropdown'),
    path('cart/update/<int:item_id>/', ad_vs.update_quantity, name='update_quantity'),
    path('cart/remove/<int:item_id>/', ad_vs.remove_item, name='remove_item'),  
    path('cart-data/', ad_vs.get_cart_data, name='get_cart_data'),
  
]
