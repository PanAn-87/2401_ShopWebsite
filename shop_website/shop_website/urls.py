"""
URL configuration for shop_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app01.views import account,shop,cart_order,SQL

urlpatterns = [
    # Default:admin後台
    path('admin/', admin.site.urls),

    # 登入、登出、註冊
    path('login/', account.login),
    path('logout/', account.logout),
    path('register/', account.register),

    # 會員資料、我的訂單
    path('mix_shop/user_info/', account.user_info),
    path('mix_shop/user_info/change/', account.user_info_change),
    path('mix_shop/order_list/', cart_order.order_list),
    path('mix_shop/order_list/<int:nid>/', cart_order.order_info),

    # 商店主頁、列表
    path('mix_shop/homepage/', shop.all_product_list),
    path('mix_shop/homepage/<int:nid>/', shop.product_list),

    # 商品詳情
    path('mix_shop/<int:nid>/product/', shop.view_product),

    # SQL查詢頁面
    path('mix_shop/sql_page/', SQL.sql_page),
    
    # 購物車
    path('mix_shop/cart_list/', cart_order.cart_list),
    path('mix_shop/cart_list/delete/', cart_order.cart_item_delete),
    path('mix_shop/cart_list/checkout/', cart_order.cart_checkout),
]

# from django.conf import settings
# from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)