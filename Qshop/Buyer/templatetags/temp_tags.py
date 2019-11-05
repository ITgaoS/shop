from django import template
register=template.Library()


@register.filter
def get_four(obj):
    return obj[:4]
@register.filter
def goods(name):
    return name.upper()



@register.filter("req")
def goods(name,a):
    name=name.replace("l",a)
    return name
@register.filter()
def Img(obj):
    return obj.replace("/media/","")