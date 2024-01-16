from django.contrib import admin
from django.utils.html import format_html

# Register your models here.

from .models import User, Tag, Product, CartItem, Order, OrderItem, ProductTag

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(CartItem)
admin.site.register(OrderItem)
# admin.site.register(ProductTag)



class OrderItemInline(admin.TabularInline):
    model = OrderItem

# 對Order後台表單作客製化
class OrderAdmin(admin.ModelAdmin):
    # 定義order表單要顯示的資料
    list_display = ('order_id', 'order_date', 'total_price', 'order_status', 'user', 'payment')
    # 定義篩選選項、admin已自帶排序功能
    list_filter = ('user_id','order_status') 

    # 在創建order時，添加額外的orderitem創立欄位
    inlines = [
        OrderItemInline,
    ]

    # 添加一個非表單中的資訊供查看 (對應到list_display中的total_peice，此項在order表單中不存在)
    def total_price(self, obj):
        # 計算 total_items_price，取得該訂單的所有 OrderItem，計算其 items_price 總和
        order_items = obj.orderitem_set.all()
        return sum(item.items_price for item in order_items)

admin.site.register(Order, OrderAdmin)

class ProductTagInline(admin.TabularInline):
    model = ProductTag
    extra = 1  # 控制要顯示多少個空白的 Tag 輸入欄位
# from django.utils.html import format_html
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'price', 'display_image', 'display_tags')
    # list_filter = ('tags')
    def display_image(self, obj):
        # 顯示產品圖片
        return format_html('<img src="{url}" width="50px" height="50px" />'.format(url=obj.product_image.url))
    # 更改顯示名稱，Default: display image
    display_image.short_description = 'Image'

    # 在創建product時，添加額外的tag創立欄位
    inlines = [
        ProductTagInline,
    ]
    def display_tags(self, obj):
        # 以逗號分隔的方式顯示商品的所有標籤
        return ', '.join(tag.tag_name for tag in obj.tags.all())
    display_tags.short_description = 'tags'

admin.site.register(Product, ProductAdmin)