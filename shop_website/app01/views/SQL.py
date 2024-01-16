from django.shortcuts import render, redirect, HttpResponse
from django.db import connection
# https://blog.csdn.net/HeatDeath/article/details/65633896

# 設定僅能用select(大或小寫)語法當開頭
def sql_page(request):
    if request.method == "GET":
        return render(request, 'sql_page.html')
    
    sql_cmd = request.POST.get("sql_cmd")
    cursor = connection.cursor()
    cursor.execute(sql_cmd)
    rows = cursor.fetchall()
    print(rows)
    return render(request, 'sql_page.html', {'rows':rows})

"""
查看與指定tag相關的商品
SELECT p.product_name, p.price
FROM app01_product AS p
JOIN app01_productTag AS pt ON p.product_id = pt.product_id
JOIN app01_tag AS t ON pt.tag_id = t.tag_id 
WHERE t.tag_id = 2;


"""