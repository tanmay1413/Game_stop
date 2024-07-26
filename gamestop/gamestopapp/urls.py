from django.urls import path
from gamestopapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.index),
    path('create_product',views.create_Product),
    path('read_Product',views.read_product),
    path('update_Product/<rid>',views.update_product),
    path('delete_product/<rid>',views.delete_Product),
    path('register',views.user_register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('create_cart/<rid>',views.create_cart),
    path('readCart',views.read_cart),  
    path('update_cart/<rid>/<q>',views.update_cart),
    path('delete_cart/<rid>', views.delete_cart),
    path('create_orders/<rid>',views.create_orders),
    path('read_order',views.read_orders),
    path('create_review/<rid>', views.create_review),
    path('read_product_detail/<rid>', views.read_product_detail),
    path('forgetpassword',views.forget_password),
    path('otpVerification',views.otp_verification),
    path('reset_password', views.reset_password),
    path('search_product',views.search_product),
    
    
    
    
    
    
    
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)