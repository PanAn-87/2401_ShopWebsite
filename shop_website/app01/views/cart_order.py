from django.shortcuts import render, redirect
from app01.models import Product, CartItem, User, Order, OrderItem
from django.db.models import Sum

def cart_list(request):
    user_id = request.session['info']['id']
    data_list = CartItem.objects.filter(user_id=user_id)
    # {'quantity__sum': 1}
    # print(data_list.aggregate(Sum('quantity')))
    sum_quantity = data_list.aggregate(Sum('quantity'))['quantity__sum']
    sum_price = data_list.aggregate(Sum('items_price'))['items_price__sum']
    return render(request, 'cart_list.html',{"data_list": data_list, "sum_quantity":sum_quantity, "sum_price":sum_price})

def cart_item_delete(request):
    nid = request.GET.get("nid")
    CartItem.objects.filter(cartitem_id=nid).delete()
    return redirect('/mix_shop/cart_list/')

def cart_checkout(request):
    user_id = request.session['info']['id']
    data_list = CartItem.objects.filter(user_id=user_id)
    sum_quantity = data_list.aggregate(Sum('quantity'))['quantity__sum']
    sum_price = data_list.aggregate(Sum('items_price'))['items_price__sum']
    user = User.objects.filter(user_id=user_id).first()
    if request.method == "GET":
        return render(request, 'cart_checkout.html', {"data_list": data_list,         
                                                  "sum_quantity":sum_quantity, 
                                                  "sum_price":sum_price,
                                                  "obj":user})
    name = request.POST.get("name")
    phone = request.POST.get("phone")
    address = request.POST.get("address")
    payment = request.POST.get("payment")
    sum_price = data_list.aggregate(Sum('items_price'))['items_price__sum']

    if not(name and address and phone):
        return render(request, 'cart_checkout.html', {"data_list": data_list,         
                                                  "sum_quantity":sum_quantity, 
                                                  "sum_price":sum_price,
                                                  "obj":user,
                                                  "error_msg": "請完成填寫"})

    # 1. 創建Order
    new_order = Order.objects.create(user_id=user_id, payment=payment, total_price=sum_price,
                         name=name, phone_number=phone, address=address)
    
    # 2. 把購物車品項轉成該訂單的品項
    user_cartitem = CartItem.objects.filter(user_id=user_id)
    for item in user_cartitem:
        OrderItem.objects.create(product=item.product, quantity=item.quantity, items_price=item.items_price, order=new_order)
    
    # 3. 刪除該用戶購物車品項
    user_cartitem.delete()
    
    return redirect('/mix_shop/cart_list/')

def order_list(request):
    user_id = request.session['info']['id']
    data_list = Order.objects.filter(user_id=user_id)
    return render(request, 'order_list.html', {"data_list": data_list})

def order_info(request, nid):
    item_list = OrderItem.objects.filter(order_id=nid)
    order = Order.objects.filter(order_id=nid).first()
    sum_quantity = item_list.aggregate(Sum('quantity'))['quantity__sum']
    sum_price = item_list.aggregate(Sum('items_price'))['items_price__sum']
    return render(request, 'order_info.html', {"item_list": item_list, "order": order,
                                               "sum_quantity":sum_quantity, "sum_price":sum_price})