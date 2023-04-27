from django.urls import path
from.import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
   path('',views.index,name='index'),
    path('registration',views.registration,name='registration'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('cust_logout',views.cust_logout,name='cust_logout'),
    path('cart',views.cart,name='cart'),
    #path('cart1',views.cart1,name='cart1'),
    path('checkout',views.checkout,name='checkout'),
    path('contact',views.contact,name='contact'),
    path('detail/<str:product_id>/',views.detail,name='detail'),
    path('detail1/<str:product_id>/',views.detail1,name='detail1'),
    path('shop',views.shop,name='shop'),
    path('shopc',views.shopc,name='shopc'),
    path('index1',views.index1,name='index1'),
    path('customer',views.customer,name='customer'),
    path('order_details',views.order_details,name='order_details'),
    path('categories',views.categories,name='categories'),
    path('dailysheet',views.dailysheet,name='dailysheet'),
    path('payment',views.payment,name='payment'),
    path('products',views.products,name='products'),
    path('orders',views.orders,name='orders'),
    path('cust_login',views.cust_login,name='cust_login'),
    path('del_product/<str:product_id>/',views.del_product,name='del_product'),
    path('del_dailysheet/<str:daily_id>/',views.del_dailysheet,name='del_dailysheet'),
    path('edit_products/<str:product_id>/',views.edit_products,name='edit_products'),
    path('add_daily',views.add_daily,name='add_daily'),
    path('add_newproduct',views.add_newproduct,name='add_newproduct'),
    path('edit_category/<str:category_id>/',views.edit_category,name='edit_category'),
    path('add_categories',views.add_categories,name='add_categories'),
    path('edit_orderdetails/<str:orderdetails_id>/',views.edit_orderdetails,name='edit_orderdetails'),
    path('edit_order/<str:order_id>/',views.edit_order,name='edit_order'),
    path('del_categories/<str:category_id>/',views.del_categories,name='del_categories'),
    path('cust_index/',views.cust_index,name='cust_index'),
    path('add_cart/<str:product_id>/',views.add_cart,name='add_cart'),
    path('remove/<str:product_id>/',views.remove,name='remove'),
    path('mens_wear',views.mens_wear,name='mens_wear'),
    path('girlswear',views.girlswear,name='girlswear'),
    path('kidswear',views.kidswear,name='kidswear'),
    path('mens_wear1',views.mens_wear1,name='mens_wear1'),
    path('girlswear1',views.girlswear1,name='girlswear1'),
    path('kidswear1',views.kidswear1,name='kidswear1'),
    path('cust_profile',views.cust_profile,name='cust_profile'),
    path('password_recovery',views.password_recovery,name='password_recovery'),
    path('banking_register',views.banking_register,name='banking_register'),
    path('ordersuccess',views.ordersuccess,name='ordersuccess'),
    #path('addshippingaddress',views.addshippingaddress,name='addshippingaddress'),
    path('check',views.check,name='check'),
    path('cust_payment',views.cust_payment,name='cust_payment'),
    #path('update_stock',views.update_stock,name='update_stock'),
    path('Ordershistory',views.Ordershistory,name='Ordershistory'),
    path('detailed_orderhistory/<str:order_id>/',views.detailed_orderhistory,name='detailed_orderhistory'),
    path('save_stock',views.save_stock,name='save_stock'),
     path('queries',views.queries,name='queries'),
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#urls.py