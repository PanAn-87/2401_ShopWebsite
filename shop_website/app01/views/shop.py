from django.shortcuts import render, redirect
from app01.models import Product, CartItem, User, Tag

# homepage: 顯示所有商品
def all_product_list(request):
    data_list = Product.objects.all()
    tag_list = Tag.objects.all()
    return render(request, 'homepage.html', {"data_list": data_list, "tag_list": tag_list})

# 商品列表: homepage/*/
def product_list(request, nid):
    data_list = Product.objects.filter(tags=nid)
    return render(request, 'homepage.html', {"data_list": data_list})

# */product: 顯示商品詳情、加入購物車(判斷:已存在->+數量、未存在->create)
def view_product(request, nid):
    if request.method == "GET":
        object = Product.objects.filter(product_id=nid).first()
        return render(request, 'product_detail.html', {"obj": object})
    
    post_quantity = int(request.POST.get("quantity"))

    # user_id = request.session['info']['id']
    user_get = request.session.get('info')
    # 點擊加入購物車的按鈕非連結而是執行動作，所以不會執行中間件跳回登入，且因沒有session直接賦予session的值會導致錯誤
    if not user_get:
        return redirect("/login/")
    user_id = user_get['id']

    # 如果購物車品項已存在，則把數量加到該資料中
    cartitem = CartItem.objects.filter(product=nid, user=user_id)
    if cartitem: # 後臺進行update時會調用CartItem的save函式，自己只有create時會
        item_quantity = cartitem.first().quantity
        item_quantity += post_quantity
        cartitem.update(quantity=item_quantity)
        cartitem.first().save() # CartItem的save函式中已包含calculate_total_price
    else:
        user = User.objects.get(user_id=user_id)
        product = Product.objects.get(product_id=nid)
        CartItem.objects.create(quantity=post_quantity, user=user, product=product)
    
    return redirect(f"/mix_shop/{nid}/product/", nid)