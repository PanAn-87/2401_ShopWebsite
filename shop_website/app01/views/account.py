from django.shortcuts import render, HttpResponse, redirect
from django import forms
from app01 import models

class LoginForm(forms.Form):
    account = forms.CharField(
        label="帳戶名稱",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"帳號名稱"}),
        required = True  # Default
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"密碼"})
    )

# 登入
def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html',{'form':form})
    
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 驗證成功，得到的帳戶和密碼
        # print(form.cleaned_data) : {'account': 'panan', 'password': '123'}

        # 去數據庫驗證帳號和密碼是否正確，獲取用戶對象
        user_object = models.User.objects.filter(**form.cleaned_data).first()
        if not user_object:
            form.add_error("password","用戶名或密碼錯誤")
            return render(request, 'login.html', {'form': form})
        
        # 帳號密碼正確
        # 網站生成隨機字符串，寫到用戶瀏覽器的cookie中，在寫入session中
        # request.session["info"] = user_object.account
        request.session["info"] = {'id':user_object.user_id, 'account':user_object.account}
        return redirect("/mix_shop/homepage/")
    return render(request, 'login.html',{'form':form})

# 登出
def logout(request):
    request.session.clear()

    return redirect('/mix_shop/homepage/')

# 註冊
def register(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'register.html',{'form':form})
    form = LoginForm(data=request.POST)
    if form.is_valid():

        # 檢查帳號是否重複
        #
        user_object = models.User.objects.filter(account=form.cleaned_data['account']).first()
        if user_object:
            form.add_error("account", "帳號已存在")
            return render(request, 'register.html', {'form': form})
        
        # 建立帳號成功
        new_user_object = models.User.objects.create(
            account=form.cleaned_data['account'],
            password=form.cleaned_data['password'],
        )
        request.session["info"] = {'id':new_user_object.user_id, 'account':new_user_object.account}
        return redirect("/mix_shop/homepage/")
    
    return render(request, 'register.html', {'form': form})

def user_info(request):
    user_id = request.session['info']['id']
    user_obj = models.User.objects.filter(user_id=user_id).first()
    return render(request, 'user_info.html', {"obj": user_obj})

def user_info_change(request):
    user_id = request.session['info']['id']
    if request.method == "GET":
        user_obj = models.User.objects.filter(user_id=user_id).first()
        return render(request, 'user_info_change.html', {"obj": user_obj})
    name = request.POST.get("name")
    phone = request.POST.get("phone")
    address = request.POST.get("address")

    models.User.objects.filter(user_id=user_id).update(name=name, 
                                                       phone_number=phone,
                                                       address=address)
    return redirect('/mix_shop/user_info/')