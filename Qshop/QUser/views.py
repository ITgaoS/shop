from QUser.models import *
import hashlib
# Create your views here.
def set_password(password):
    md5=hashlib.md5()
    md5.update(password.encode())
    result=md5.hexdigest()
    return result
def valid_user(email):
    try:
        user=User.objects.get(email=email)
    except Exception as e:
        return False
    else:
        return user
def add_user(**kwargs):
    if "email" in kwargs and "username" not in kwargs:
        kwargs["username"]=kwargs["email"]
    user =User.objects.create(**kwargs)
    return user


def updata_user(id,**kwargs):
    pass
def delete_user(id):
    pass