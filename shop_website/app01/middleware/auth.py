from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
import re

class AuthMiddleware(MiddlewareMixin):
    # 允許的網址和動態網址
    allowed_path = ['/mix_shop/homepage/',
                    '/login/',
                    '/register/',]
    allowed_re_path = [re.compile(r'/mix_shop/\d+/product/'),
                       re.compile(r'/mix_shop/homepage/\d+/')]
    
    def process_request(self, request):
        # 0.排除那些不需要登入就能訪問的頁面
        # request.path_info 取得當前用戶請求的URL (/login/)
        if request.path_info in self.allowed_path:
            # print(request.path_info)
            return
        elif request.path_info.startswith('/admin/'): # 後台，與前一個if作用相同，方便刪減，startswith:bool
            return
        elif request.path_info == '/': # 指輸入ip時回首頁
            return redirect('/mix_shop/homepage/')
        else:
            for re_path in self.allowed_re_path:
                if re_path.match(request.path_info):
                    return

        # 1.讀取當前用戶的session信息，如果能讀到，說明已登入過，便可繼續下一步
        info_dict = request.session.get("info")
        # print(info_dict)
        if info_dict:
            return
        
        # 2.未登入過，重新回到登入介面
        return redirect('/login/')