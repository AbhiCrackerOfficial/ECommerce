from django.contrib import admin
from django.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="home"),
    path('cart/', views.cart, name="Cart"),
    path('shop/', views.shop, name="Shop"),
    path('checkout/', views.checkout, name="Checkout"),
    path('profile/', views.profile, name="Profile"),
    path('payment/', views.payment, name="Payment"),
    path('signin/', views.signin, name="Sign In"),
    path('signup/', views.signup, name="Sign Up"),
    path('forgot_password/', views.forgot, name="Forgot Password"),
    path('reset_password/', views.reset, name="Reset Password"),
    path('logout/', views.signout, name="SignOut"),
    path('check_user_exists/', views.check_user_existence,
         name='check_user_exists'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('search/', views.search, name='search'),
    path('otp/', views.verify_otp, name='verify_otp'),
    path('submit_otp/', views.submit_otp, name='submit_otp'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('add_to_cart/<int:product_id>/',
         views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/',
         views.remove_from_cart, name='remove_from_cart'),
    path('change_quantity/<int:product_id>/<str:operation>/',
         views.change_quantity, name='change_quantity'),
    path('order_confirmation/', views.order_confirmation,
         name='order_confirmation'),
    path('payment/<str:operation>/', views.paycheck, name='paycheck'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
