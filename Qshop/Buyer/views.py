from django.shortcuts import render,HttpResponseRedirect
from django.http import JsonResponse

from Shop.models import GoodsType,Goods
from Buyer.models import *
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
    if email:
        now_data=History.objects.filter(user_email=email).order_by("id")
        if len(now_data)>=5:
            now_data[0].delete()
        history=History()
        history.user_email=email
        history.goods_id=id
        history.goods_name=good_data.name
        history.goods_price=good_data.price
        history.goods_picture=good_data.picture
        history.save()
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
    request.session.clear()

    return response
@login_valid
def cart(request):
    email=request.COOKIES.get("email")
    goods_list=BuyCar.objects.filter(car_user=email)
    count=len(goods_list)
    if request.method=="POST":
        data=request.POST
        post_data=[]
        for key in data:
            if key.startswith("check"):
                id=key.split("_")[1]
                num="number_%s"%id
                number=data[num]
                post_data.append((id,number))
        p_order=Pay_order()
        p_order.order_id=str(time.time()).replace(".","")
        p_order.order_number=len(post_data)
        p_order.order_user=User.objects.get(email=request.COOKIES.get("email"))
        p_order.save()
        order_total=0
        for id,number in post_data:
            number=int(number)
            goods=Goods.objects.get(id=int(id))
            o_info=Order_info()
            o_info.order_id=p_order
            o_info.goods_name=goods.name
            o_info.goods_number=number
            o_info.goods_price=goods.price
            o_info.goods_total=number*goods.price
            o_info.goods_picture=goods.picture.url
            o_info.order_store=goods.good_store
            o_info.save()
            order_total+=o_info.goods_total
        p_order.order_total=order_total
        p_order.save()

        return HttpResponseRedirect("/Buyer/place_order/?order_id=%s"%p_order.order_id)
    return render(request,"buyer/cart.html",locals())
def pay_order(request):
    email = request.COOKIES.get("email")
    order_id=request.GET.get("order_id")
    addr=GoodsAddress.objects.all()
    if order_id:
        p_order=Pay_order.objects.get(order_id=order_id)
        order_info=p_order.order_info_set.all()
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

    order_id=request.GET.get("out_trade_no")
    pay_order=Pay_order.objects.get(order_id=order_id)
    pay_order.order_state=1
    pay_order.save()
    return render(request,"Buyer/pay_result.html",locals())
@login_valid
def user_center_info(request):
    user_email=request.COOKIES.get("email")
    user=User.objects.get(email=user_email)
    goods_list=History.objects.filter(user_email=user_email)
    return render(request,"buyer/user_center_info.html",locals())


def add_car(request):
    result={"state":"error","data":""}
    if request.method=="POST":
        user=request.COOKIES.get("email")
        if user:
            goods_id=request.POST.get("goods_id")
            number=request.POST.get("number",1)
            try:
                goods=Goods.objects.get(id=goods_id)
            except Exception as e:
                result["data"]=str(e)
            else:
                car=BuyCar()
                car.car_user=user
                car.goods_name=goods.name
                car.goods_picture=goods.picture
                car.good_price=goods.price
                car.good_number=number
                car.good_total=int(number)*goods.price
                car.good_store = goods.good_store.id
                car.goods_id=goods_id
                car.save()
                result["state"]="success"
                result["data"]="加入购物车成功"
        else:
            result["data"]="用户未登录 无法添加"
    return JsonResponse(result)


from QUser.models import GoodsAddress
def user_center_site(request):
    email=request.COOKIES.get("email")
    user=User.objects.get(email=email)
    addr=user.goodsaddress_set.filter(state=1)[0]
    if request.method=="POST":
        recv=request.POST.get("recv")
        address=request.POST.get("address")
        post_number=request.POST.get("post_number")
        phone=request.POST.get("phone")
        addr=GoodsAddress()
        addr.recver=recv
        addr.address=address
        addr.post_number=post_number
        addr.phone=phone
        addr.state=0
        addr.user=user
        addr.save()
    return render(request,"buyer/user_center_site.html",locals())


def  user_center_order(request):
    email=request.COOKIES.get("email")
    user=User.objects.filter(email=email).first()
    if user:
        order_list = user.pay_order_set.all()

    return render(request,"buyer/user_center_order.html",locals())


