from django.db import models

# Create your models here.
class User(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=32)
    username = models.CharField(max_length=32,blank=True,null=True)
    gender=models.CharField(blank=True,max_length=8,null=True)
    age=models.IntegerField(blank=True,null=True)
    phone=models.CharField(blank=True,max_length=32,null=True)
    address=models.CharField(blank=True,null=True,max_length=48)
    picture=models.ImageField(upload_to="images",default="images/gougou.png")
    identity=models.IntegerField(default=0)

