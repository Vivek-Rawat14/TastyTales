from django.db import models



allProducts = (('videos','Videos'),('books','Books'),('burger', 'Burger'), ('pizza', 'Pizza'), ('noodles', 'Noodles'),  ('biryani', 'Biryani'),
               ('ice cream', 'Ice cream'), ('sweet', 'Sweet'), ('northfood', 'Northfood'), ('southfood', 'Southfood'),  ('topfood', 'Topfood'))



# Create your models here.
class recipes(models.Model):
    foodname = models.CharField(max_length=255)
    foodimg = models.ImageField()
    foodinfo = models.TextField( default="No information available") 
    foodprice = models.IntegerField(null=True,blank=True)
    videoSrc = models.URLField(null=True,blank=True,max_length=500)
    category = models.CharField(choices=allProducts, max_length=255)

class users(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    repassword = models.CharField(max_length=100,null=True)
    address = models.TextField()
    pincode = models.IntegerField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)    
    cart = models.CharField(max_length=255,default='[]')
    likes = models.CharField(max_length=255,default='[]')
    likesv = models.CharField(max_length=255,default='[]')
    likesr = models.CharField(max_length=255,default='[]')