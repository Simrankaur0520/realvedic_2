from django.contrib import admin
from django.urls import path
import realvedic_app.views as views 

from django.conf.urls.static import static
from django.conf import settings

import realvedic_app.auth as auth
#import realvedic_app.user_data as user
import realvedic_app.cart as cart
import realvedic_app.user_account as usr
import realvedic_app.paymentgateway as pay
import realvedic_app.doctors as doc
'''import realvedic_app.admin_views as admin_views
import realvedic_app.payments as pay
import realvedic_app.order_status as od'''


urlpatterns = [
    path("write_data",views.write_data,name="write_data"),
    path("single_product_view",views.single_product_view,name="single_product_view"),
    path("categoryPage",views.categoryPage,name="categoryPage"),
    path("all_product_view",views.all_product_view,name="all_product_view"),
    #--------login and signup
    path('signUp',auth.signUp,name='signUp'),
    path('login',auth.login,name='login'),
    path('user_view',auth.user_view,name='user_view'),

    #-------cart----------------------
   
    path('add_to_cart',cart.add_to_cart,name='add_to_cart'),
    path('UserCartView',cart.UserCartView,name='UserCartView'),
    path('checkout',cart.checkout,name='checkout'),
    path('CartUpdate',cart.CartUpdate,name='CartUpdate'),
    path('CartitemDelete',cart.CartitemDelete,name='CartitemDelete'),


    #-------------------------------------------user details 
    path('userAccountView',usr.userAccountView,name='userAccountView'),
    path('UserAccountEdit',usr.UserAccountEdit,name='UserAccountEdit'),

    #---------------------------------Payment gateway------------------

    path('start_payment',pay.start_payment,name='start_payment'),
    path('handle_payment_success',pay.handle_payment_success,name='handle_payment_success'),



     path('doctor_detail_view',doc.doctor_detail_view,name='doctor_detail_view'),

    
    


]