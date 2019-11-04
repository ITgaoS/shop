from django.shortcuts import render
from django.http import HttpResponseRedirect
from QUser.views import *
from Shop.models import *
import smtplib
from email.mime.text import MIMEText


def sendMial(content, email):
    from Qshop.settings import MAIL_SENDER, MAIL_PASSWORD, MAIL_SERVER, MAIL_PORT
    content = """
        如果确认是本人修改密码，请点击下放链接进行密码修改
        <a href="%s">点击链接确认</a>
    """ % content
    print(content)
    # 构建邮件格式
    message = MIMEText(content, "html", "utf-8")
    message["To"] = email
    message["From"] = MAIL_SENDER
    message["Subject"] = "密码修改"

    # 发送邮件
    smtp = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)
    smtp.login(MAIL_SENDER, MAIL_PASSWORD)
    smtp.sendmail(MAIL_SENDER, [email], message.as_string())
    smtp.close()


# Create your views here.
def login_valid(fun):
    def inner(request, *args, **kwargs):
        cookie_user = request.COOKIES.get("email")
        session_user = request.session.get("email")
        if cookie_user and session_user and cookie_user == session_user:
            user = User.objects.get(email=cookie_user)
            identity = user.identity
            if identity >= 1:
                return fun(request, *args, **kwargs)

            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect("/Shop/login/")


    return inner


def register(request):
    """
    后台卖家注册功能
    """

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")
        error = ""
        if valid_user(email):
            error = "当前邮箱已经注册"
        else:
            password = set_password(password)
            add_user(email=email, password=password)
            return HttpResponseRedirect("/Shop/login/")
    return render(request, "shop/register.html", locals())


def login(request):
    """
    后台卖家登功能录
    :param request:
    :return:
    """
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = valid_user(email)

        if user:
            db_password = user.password
            request_password = set_password(password)
            if db_password == request_password:
                response = HttpResponseRedirect("/Shop/")
                response.set_cookie("email", user.email)
                response.set_cookie("user_id", user.id)
                request.session["email"] = user.email
                return response
            else:
                error = "密码错误"
        else:
            error = "用户不存在"

    return render(request, "shop/login.html", locals())


@login_valid
def index(request):
    """
    后台卖家首页
    """
    return render(request, "shop/index.html")


def logout(request):
    """
    后台卖家退出登录功能
    :param request:
    :return:
    """
    response = HttpResponseRedirect("/Shop/login/")
    response.delete_cookie("email")
    response.delete_cookie("user_id")
    request.session.clear()
    return response


def forget_password(request):
    """
    后台卖家忘记密码功能
    :param request:
    :return:
    """
    return render(request, "shop/forgot-password.html")


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get("email")

        if email and valid_user(email):
            print("sss")
            hash_code = set_password(email)
            contecnt = "http://127.0.0.1:8000/Shop/change_password/?email=%s&token=%s" % (email, hash_code)
            print(contecnt)
    return HttpResponseRedirect("/Shop/forget_password/")


def change_password(request):
    """
    当前人是否有资格修改密码
    """
    if request.method == "POST":
        email = request.COOKIES.get("change_email")
        password = request.POST.get("password")
        e = User.objects.get(email=email)
        e.password = set_password(password)
        e.save()
        return HttpResponseRedirect("/Shop/login/")
    # 通过get请求获得了修改密码的用户和校验值
    email = request.GET.get("email")
    token = request.GET.get("token")
    # 进行再次校验
    now_token = set_password(email)
    # 当前提交人存在，并且token值正确
    if valid_user(email) and now_token == token:
        # 返回修改密码页面
        reponse = render(request, "shop/change_password.html", locals())
        # reponse.set_cookie("change_email",email)
        return reponse
    else:
        return HttpResponseRedirect("/Shop/forget_password/")


@login_valid
def profile(request):
    user_email = request.COOKIES.get("email")
    user = User.objects.get(email=user_email)
    if request.method == "POST":
        password = request.POST.get("password")
        user.password = set_password(password)
        user.save()
        response = HttpResponseRedirect("/Shop/login/")
        response.delete_cookie("email")
        response.delete_cookie("user_id")
        return response

    return render(request, "shop/profile.html", {"user": user})


@login_valid
def set_profile(request):
    user_email = request.COOKIES.get("email")
    user = User.objects.get(email=user_email)
    if request.method == "POST":
        post_data = request.POST
        username = post_data.get("username")
        gender = post_data.get("gender")
        age = post_data.get("age")
        if age:
            user.age = age
        phone = post_data.get("phone")
        address = post_data.get("address")
        picture = request.FILES.get("picture")
        user.gender = gender

        user.phone = phone
        user.address = address
        user.username = username
        if picture:
            user.picture = picture
        user.save()
        return HttpResponseRedirect("/Shop/profile/")
    return render(request, "shop/set_profile.html", {"user": user})


@login_valid
def add_goods(request, id=0):
    type_list=GoodsType.objects.all()
    if id:
        goods = Goods.objects.get(id=id)
    if request.method == "POST":
        post_data = request.POST
        name = post_data.get("name")
        price = post_data.get("price")
        number = post_data.get("number")
        production = post_data.get("production")
        safe_date = post_data.get("safe_date")
        description = post_data.get("description")
        goods_type=post_data.get("goods_type")
        picture = request.FILES.get("picture")
        if not id:
            goods = Goods()
        goods.price = price
        goods.name = name
        goods.number = number
        goods.production = production.replace("年", "-").replace("月", "-").replace("日", "")
        goods.safe_date = safe_date
        goods.description = description
        goods.goods_type=GoodsType.objects.get(id=int(goods_type))

        store_id=request.COOKIES.get("email")
        goods.good_store=User.objects.get(email=store_id)
        if picture:
            goods.picture = picture
        goods.save()
        if id:
            return HttpResponseRedirect("/Shop/goods/%s/" % goods.id)
        return HttpResponseRedirect("/Shop/goods_list/")
    return render(request, "shop/add_goods.html", locals())


@login_valid
def goods_list(request):
    email=request.COOKIES.get("email")
    user=User.objects.get(email=email)
    goods_list=user.goods_set.all()
    return render(request, "shop/goods_list.html", locals())


@login_valid
def set_goods(request, id):
    set_type = request.GET.get("set_type")
    goods = Goods.objects.get(id=int(id))
    if set_type == "up":
        goods.statue = 1
    elif set_type == "down":
        goods.statue = 0
    goods.save()
    return HttpResponseRedirect("/Shop/goods_list/")


def goods(request, id):
    goods_data = Goods.objects.get(id=id)
    return render(request, "shop/goods.html", locals())


from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator
from Qshop.settings import PAZE_SIZE


class GoodsView(View):
    def get(self, request):
        result = {

            "version": "v1",
            "code": "200",
            "data": [],
            "page_range": [],
            "up_down": False,
        }
        id = request.GET.get("id")  # 尝试获取前端get提交的id
        # 如果id存在，获取当前id的数据
        # 尝试获取查询的值
        keywords = request.GET.get("keywords")
        # 获取所有数据

        if id:
            goods = Goods.objects.get(id=id)
            if goods.statue:
                goods.statue = 0
            else:
                goods.statue = 1
            goods.save()
            page_number = request.GET.get("page", 1)
            all_goods = Goods.objects.all().order_by("id")
            paginator = Paginator(all_goods, PAZE_SIZE)
            page_data = paginator.page(int(page_number))
            result["page_range"] = list(paginator.page_range)
            goods_data = [{
                "id": g.id,
                "name": g.name,
                "price": g.price,
                "number": g.number,
                "production": g.production,
                "safe_date": g.safe_date,
                "picture": g.picture.url,
                "description": g.description,
                "statue": ["上架" if g.statue else "下架"][0]} for g in page_data
            ]



        else:
            page_number = request.GET.get("page", 1)
            all_goods = Goods.objects.all().order_by("id")
            if keywords:  # 如果有值，查询对应值
                all_goods = Goods.objects.filter(name__contains=keywords).order_by("id")
                result["referer"] = "&keywords=%s" % keywords
            paginator = Paginator(all_goods, PAZE_SIZE)
            page_data = paginator.page(page_number)
            result["page_range"] = list(paginator.page_range)

            goods_data = [{
                "id": g.id,
                "name": g.name,
                "price": g.price,
                "number": g.number,
                "production": g.production,
                "safe_date": g.safe_date,
                "picture": g.picture.url,
                "description": g.description,
                "statue": ["上架" if g.statue else "下架"][0]  } for g in page_data
            ]

        result["data"] = goods_data
        return JsonResponse(result)


def vue_list_goods(request):

    return render(request, "shop/vue_list_goods.html")


from django.http import HttpResponse
from CeleryTask.tasks import add


def get_celery(request):
    x = 1
    y = 2
    add.delay(x, y)
    return HttpResponse("调用完成")
