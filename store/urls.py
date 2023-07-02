from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.update_item, name='update_item'),
    path('process_order/', views.process_order, name='process_order'),
    path('product/<int:pk>/', views.view_product, name='product-view'),

    # path('login/', views.login_page, name='login'),
    # path('register/', views.register_page, name='register'),
    # path('logout/', views.logout_user, name='logout')
]
