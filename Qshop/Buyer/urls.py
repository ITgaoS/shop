
from django.urls import path,re_path
from Buyer.views import *
urlpatterns = [
path("base/",base),
path("",index),
path("index/",index),
path("login/",login),
path("logout/",logout),
path("cart/",cart),
path("goods_list/",goods_list),
path('place_order/', pay_order),
path('get_pay/', get_pay),
path('add_car/', add_car),
path('ucf/', user_center_info),
path('pay_result/', pay_result),
path('resgister/', resgister),
path('ucs/', user_center_site),
path('uco/', user_center_order),
re_path("goods/(?P<id>\d+)/",goods)
]