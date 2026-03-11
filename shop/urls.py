from django.urls import path
from.import views

urlpatterns = [
  path('search_products/', views.search_products, name="search_products"),
  path('search/', views.search, name="search"),
  path('', views.home, name='home'),
  path('register',views.register,name='register'),
  path('collection',views.collection,name='collection'),
  path('collections/<str:name>/',views.collectionsview,name='collections'),
  path('collections/<str:cname>/<str:pname>',views.products_ditails,name='products_name'),
  path('login',views.login,name='login'),
  path('logout',views.logout,name='logout'),
  path('add_to_cart',views.add_to_cart, name='add_to_cart'),
  path('cart_page',views.cart_page,name='cart_page'),
  path('remove_from_cart/<str:cid>',views.remove_from_cart,name='remove_from_cart'),
  
]