from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
class MiddleWareIp(MiddlewareMixin):
    # def process_request(self,request):
    #     request_ip=request.META["REMOTE_ADDR"]
    #     if request_ip=="127.0.0.1":
    #         return HttpResponse("非法ip")
    def process_exception(self,request,exception):
        print(exception)
        import os
        import datetime
        from Qshop.settings import BASE_DIR
        log_path=os.path.join(BASE_DIR,"error.log")
        with open(log_path,"a") as  f:
            now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content="[%s]:%s\n"%(now,str(exception))
            f.write(content)
        print("我是process_exception")
    def process_template_response(self,resquest,response):
        print("我是process_temp_response")
        return response
    def process_response(self,resquest,response):
        for method in dir(response):
            if not method.startswith("_"):
                print(method)
            response.set_cookie("hello","world")
            return response