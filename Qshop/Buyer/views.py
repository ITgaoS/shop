from django.shortcuts import render,HttpResponseRedirect
from Shop.models import GoodsType,Goods
from Shop.views import valid_user,set_password
from QUser.models import *
def login_valid(fun):
    def inner(request,*args,**kwargs):
        referer=request.GET.get("referer")
        cookie_user=request.COOKIES.get("email")
        session_user=request.session.get("email")
        if cookie_user and session_user and cookie_user==session_user:
            return fun(request,*args,**kwargs)
        else:
            login_url="/Buyer/login/"
            if referer:
                login_url="/Buyer/login/?referer=%s"% referer
            return HttpResponseRedirect(login_url)
    return inner
def base(request):
    message="hello"
    return render(request,"buyer/base.html",locals())
def index(request):
    email = request.COOKIES.get("email")
    type_data=[]
    type_list=GoodsType.objects.all()
    for i in type_list:
        data=GoodsType.objects.hello(id=i.id)
        type_data.append(data)
    print(type_data)
    return render(request, "buyer/index.html",locals())
def goods_list(request):
    email = request.COOKIES.get("email")
    id=request.GET.get("id")
    goods_list=Goods.objects.filter(statue=1,good_store=2)
    if id:
        goods_type=GoodsType.objects.get(id=int(id))
        goods_list=goods_type.goods_set.filter(statue=1,good_store=2)
    return render(request,"buyer/list.html",locals())
def goods(request,id):
    email = request.COOKIES.get("email")
    good_data=Goods.objects.get(id=int(id))
    return render(request,"buyer/goods.html",locals())

# def login(request):
#     get_referer=request.META.get("HTTP_REFERER")
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("pwd")
#         # 判断用户是否存在
#         # 如果存在
#         user = valid_user(email)
#         if user:
#             # 判断密码是否正确
#             db_password = user.password
#             request_password = set_password(password)
#             if db_password == request_password:
#                 referer=request.POST.get("referer")
#                 response = HttpResponseRedirect(referer)
#                 response.set_cookie("email", user.email)
#                 response.set_cookie("user_id", user.id)
#                 request.session["email"] = user.email
#                 return response
#             else:
#                 error = "密码错误"
#         else:
#             error = "用户不存在"
#     return render(request, "buyer/login.html", locals())resgisterm
def resgister(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        email=request.POST.get("email")
        is_email=None
        try:
            is_email=User.objects.get(email=email)
        except:
            password
        if  not is_email:
            user=User()
            user.username=username
            user.password=set_password(password)
            user.email=email
            user.save()
            error="注册成功 请去登录"
        else:
            error = "已注册 请去登录"


    return render(request,"buyer/register.html",locals())
def login(request):
    referer=request.GET.get("referer")
    if not referer:
        referer=request.META.get("HTTP_REFERER")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("pwd")
        # 判断用户是否存在
        # 如果存在
        user = valid_user(email)
        if user:
            # 判断密码是否正确
            db_password = user.password
            request_password = set_password(password)
            if db_password == request_password:
                if request.POST.get("referer"):
                    referer=request.POST.get("referer")
                if referer in ('http://127.0.0.1:8000/Buyer/login/',"None","http://127.0.0.1:8000/Buyer/resgister/"):
                    referer = "/Buyer/"
                response = HttpResponseRedirect(referer)
                response.set_cookie("email", user.email)
                response.set_cookie("user_id", user.id)
                request.session["email"] = user.email
                return response
            else:
                error = "密码错误"
        else:
            error = "用户不存在"
    return render(request, "buyer/login.html", locals())
def logout(request):
    response=HttpResponseRedirect("/Buyer/index/")
    response.delete_cookie("email")
    response.delete_cookie("user_id")
    return response
@login_valid
def cart(request):
    email=request.COOKIES.get("email")
    return render(request,"buyer/cart.html",locals())
def pay_order(request):
    email = request.COOKIES.get("email")
    return render(request,"buyer/place_order.html",locals())
import time
from Buyer.zhifu import Pay
def get_pay(request):
    order_number=str(time.time()).replace(".",",")
    order_price="666.6"
    url=Pay(order_number,order_price)
    return HttpResponseRedirect(url)
def pay_result(request):
    email = request.COOKIES.get("email")
    data=request.GET
    return render(request,"Buyer/pay_result.html",locals())