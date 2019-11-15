from django.views.decorators.cache import cache_page
from django.urls import path,re_path,include
from Shop.views import *


urlpatterns=[
    re_path(r"^$",index),
    path("index/",index),
    path("register/",register),
    path("login/",login),
    path("logout/",logout),
    path("forget_password/",forget_password),
    path("reset_password/", reset_password),
    path("change_password/", change_password),
    path("profile/",profile),
    path("set_profile/",set_profile),
    path("add_goods/",add_goods),
    re_path("^add_goods/(?P<id>\d+)",add_goods),
    path("goods_list/",goods_list),
    re_path(r"^set_goods/(?P<id>\d+)/",set_goods),
    re_path(r"^goods/(?P<id>\d+)/",goods),
    path("ckeditor/",include("ckeditor_uploader.urls")),
    re_path("Goods/",GoodsView.as_view()),
    path("vue_list_goods/",vue_list_goods),
    path("order_list/",order_list),
    path("send_shop/",send_shop),
    path("return_goods_number/",return_goods_number)
 ]

urlpatterns=urlpatterns+[
    path("get_celery/", get_celery),
    path("get_address/", get_address),
]