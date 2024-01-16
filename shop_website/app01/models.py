from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

# Create your models here.
# python manage.py makemigrations
# python manage.py migrate

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    account = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    # 顯示object+id改為顯示user_name
    def __str__(self): 
        return f"id:{self.user_id}, name:{self.account}"

class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=20)
    def __str__(self):
        return f"id:{self.tag_id}, {self.tag_name}"
    
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=20, unique=True)
    price = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)
    product_image = models.ImageField(upload_to='image/')
    tags = models.ManyToManyField(Tag, through='ProductTag')
    def __str__(self):
        return f"{self.product_name}, NT$ {self.price}"
    
class CartItem(models.Model):
    cartitem_id = models.AutoField(primary_key=True)
    quantity = models.PositiveIntegerField()
    items_price = models.PositiveIntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # 計算數值並在保存資料時賦予給items_price(=quantity*price)
    def save(self, *args, **kwargs):        
        self.calculate_total_price()
        super().save(*args, **kwargs)

    # 計算 total_price，product.price * quantity
    def calculate_total_price(self):
        self.items_price = self.product.price * self.quantity
    class Meta:
        unique_together = ('product', 'user')
    # 更改顯示方式
    def __str__(self):
        return f"id: {self.user.account} 用戶: {self.user.account} {self.product.product_name}*{self.quantity}，共 NT${self.items_price}"
    

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_date = models.DateField(auto_now_add=True)
    total_price = models.PositiveIntegerField(null=True, blank=True)
    ORDER_STATUS = [('not_processed', '尚未處理'),
        ('in_progress', '處理中'),
        ('completed', '已完成')]
    order_status = models.CharField(max_length=20,choices=ORDER_STATUS,default='not_processed')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    PAYMENT_METHOD= [('pay_on_delivery', '貨到付款'),
                     ('bank_transfer', '銀行轉帳'),
                     ('credit_card_payment', '信用卡支付')]
    payment = models.CharField(max_length=20,choices=PAYMENT_METHOD)
    name = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    
    def get_order_status_display(self):
        return dict(self.ORDER_STATUS).get(self.order_status, self.order_status)

    def get_payment_display(self):
        return dict(self.PAYMENT_METHOD).get(self.payment, self.payment)

    def __str__(self):
        return f"訂單ID: {self.order_id}, 用戶: {self.user.account}, 總額: {self.total_price}, 日期: {self.order_date}"


class OrderItem(models.Model):
    orderitem_id = models.AutoField(primary_key=True)
    quantity = models.PositiveIntegerField()
    items_price = models.PositiveIntegerField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order,null=True, blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # 在保存前計算 total_price
        self.calculate_total_price()
        super().save(*args, **kwargs)

    def calculate_total_price(self):
        # 計算 total_price，product.price * quantity
        if self.product and self.quantity is not None:
            self.items_price = self.product.price * self.quantity
        else:
            self.items_price = None
    def __str__(self):
        return f"{self.product} - Quantity: {self.quantity}, Total Price: {self.items_price}"
    class Meta:
        unique_together = ('product', 'order')
    def __str__(self):
        return f"{self.order.order_id} 訂單品項: {self.product.product_name}*{self.quantity}，共 NT${self.items_price}"
    
# 因為要設置unique，不然可以省略(Django會自動幫創建)
class ProductTag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'tag')