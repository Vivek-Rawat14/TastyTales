import json
from django.http import JsonResponse
from django.shortcuts import render ,redirect
from django.core.paginator import Paginator
import requests
from .models import recipes,users
from django.contrib import messages
from . import models


# Create your views here.
def homepage(req):
    if 'user' not in req.session:
        return redirect('/login')
    response = requests.get('https://dummyjson.com/recipes', {"limit": 100})
    ca = response.json()["recipes"]
    db =recipes.objects.filter(category="topfood").values()
    cl= list(db)
    for i in cl:
             i.update({'foodimg': i['foodimg'].split('_')[
                0]+i['foodimg'].split('_')[1][-4:]})
    d = recipes.objects.filter(category='videos').values()
    c=list(d)
    b = recipes.objects.filter(category='books')
    l = list(b)
    return render(req, 'index.html',context={"rece":ca,"data":cl,"da":c,"cd":l})

def recipe(req):
  
    response = requests.get('https://dummyjson.com/recipes', {"limit": 100})
    cl = response.json()["recipes"]
    
 
    paginator = Paginator(cl, 12)
   
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    return render(req, 'recipe.html', context={'data': page_obj})

def recipeshow(req,Id):
     response = requests.get(f'https://dummyjson.com/recipes/{Id}')
     cl = response.json()
     return render(req,'recipeshow.html',context={"data":cl})

def video(req):
    db = recipes.objects.filter(category='videos')
    paginator = Paginator(db, 12 )  

    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number) 

    return render(req, 'video.html', context={"data": page_obj})



def videoshow(req,Id):
    db = recipes.objects.filter(id=Id).values()
    cl= list(db)
    return render(req,'videoshow.html',context={"data":cl})

def books(req):
    db = recipes.objects.filter(category='books')
    cl = list(db)
    return render(req,'books.html',context={"data":cl})

def orderfood(req):
    a = recipes.objects.filter(category='topfood').values()
    cl = list(a)
    for i in cl:
             i.update({'foodimg': i['foodimg'].split('_')[0] + i['foodimg'].split('_')[1][-4:]})
    return render(req,'orderfood.html',context={'data':cl})

def ordershow(req,Id):
     a = recipes.objects.filter(id=Id).values()
     b = list(a)
     return render(req,'ordershow.html',context={'data':b})

def buyconto(req,Id):
    db =recipes.objects.filter(id=Id).values()
    cl= list(db)
    for i in cl:
             i.update({'foodimg': i['foodimg'].split('_')[
                0]+i['foodimg'].split('_')[1][-4:]})
    return render(req,'byconto.html',context={"data":cl})
     

def burger(req):
    a = recipes.objects.filter(category='burger').values()
    cl = list(a)
    return render(req,'burger.html',context={'data':cl})


def pizza(req):
    a = recipes.objects.filter(category='pizza').values()
    cl = list(a)
    return render(req,'pizza.html',context={'data':cl})


def sweet(req):
    a = recipes.objects.filter(category='sweet').values()
    cl = list(a)
    return render(req,'sweet.html',context={'data':cl})




def northfood(req):
    a = recipes.objects.filter(category='northfood').values()
    cl = list(a)
    return render(req,'northfood.html',context={'data':cl})



def southfood(req):
    a = recipes.objects.filter(category='southfood').values()
    cl = list(a)
    return render(req,'southfood.html',context={'data':cl})


def noodles(req):
    a = recipes.objects.filter(category='noodles').values()
    cl = list(a)
    return render(req,'chinese.html',context={'data':cl})


def icecream(req):
    a = recipes.objects.filter(category='ice cream').values()
    cl = list(a)
    return render(req,'ice.html',context={'data':cl})



def biryani(req):
    a = recipes.objects.filter(category='biryani').values()
    cl = list(a)
    return render(req,'biryani.html',context={'data':cl})

def signup(req):
     if req.method=="POST":
        name = req.POST['name']
        phone = req.POST['phone']
        email = req.POST['email']
        password = req.POST['password']
        confirm_password = req.POST['confirm_password']
        address = req.POST['address']
        city = req.POST['city']
        state = req.POST['state']
        pincode = req.POST['pincode']
        
        if password != confirm_password:
            messages.error(req, "Passwords do not match.")
            return render(req, 'signup.html')
        
        if users.objects.filter(email=email).exists():
            messages.error(req, "Email is already registered.")
            return render(req, 'signup.html')
        
        users.objects.create(username = name,password=password,email=email,phone =phone,address= address,city=city,pincode=pincode,state=state,repassword=confirm_password  )
        messages.success(req, "Signup successful. Please log in.")
        return redirect('/login')
     return render(req,'signup.html')

def login(req):
    if req.method == "POST":
        phonenumber = req.POST.get('phone')
        password = req.POST.get('password')

        try:
            s = users.objects.get(phone=phonenumber)
            if s.password == password: 
                req.session['user'] = s.username  
                return redirect('/')
            else:
                return render(req, 'login.html', {"error": "Invalid password"})
        except users.DoesNotExist:
            return render(req, 'login.html', {"error": "User not found"})
        except Exception as e:
            return render(req, 'login.html', {"error": "Something went wrong, try again"})

    return render(req, 'login.html')

def profile(req):
    if 'user' not in req.session:
        return redirect('/login')

    username = req.session['user']
    try:
        user_data = users.objects.filter(username=username).values()
        return render(req, 'profile.html', context={"userde": user_data})
    except users.DoesNotExist:
        return render(req, 'profile.html', context={"error": "User not found"})


def addlikeitemv(req, Id):
    if 'user' not in req.session:
        return redirect('/login')

    try:
        user = models.users.objects.get(username=req.session['user'])
        liked = json.loads(user.likesv or '[]')  # handle None or empty
        
        if str(Id) not in liked:
            liked.append(str(Id))
            user.likesv = json.dumps(liked)
            user.save()
            
        return redirect('/videolike')

    except models.users.DoesNotExist:
        return redirect('/login')

def videolike(req):
    if 'user' not in req.session:
        return redirect('/homepage')
    
    username = req.session['user']
    try:
        user = users.objects.get(username=username)

        try:
            liked_ids = json.loads(user.likesv)  # convert string to list
        except json.JSONDecodeError:
            liked_ids = []

        liked_items = recipes.objects.filter(id__in=liked_ids)
        return render(req, 'videolike.html', context={'data': liked_items})
    except users.DoesNotExist:
        return redirect('/login')


def addlikeitemrs(req, Id):
    if 'user' not in req.session:
        return redirect('/homepage')

    username = req.session['user']
    try:
        user = users.objects.get(username=username)

        try:
            liked_ids = json.loads(user.likesr or '[]')
        except json.JSONDecodeError:
            liked_ids = []

        if str(Id) not in liked_ids:
            liked_ids.append(str(Id))
            user.likesr = json.dumps(liked_ids)
            user.save()

        return redirect('/recipelike')

    except users.DoesNotExist:
        return redirect('/login')



def recipelike(req):
    if 'user' not in req.session:
        return redirect('/homepage')

    username = req.session['user']
    try:
        user = users.objects.get(username=username)

        try:
            liked_ids = json.loads(user.likesr or '[]')
        except json.JSONDecodeError:
            liked_ids = []

        liked_recipes = []
        for rid in liked_ids:
            try:
                response = requests.get(f"https://dummyjson.com/recipes/{rid}")
                if response.status_code == 200:
                    liked_recipes.append(response.json())
            except:
                continue

        return render(req, 'recipelike.html', {'data': liked_recipes})

    except users.DoesNotExist:
        return redirect('/login')

def addlikeitem(req, Id):
    if 'user' not in req.session:
        return redirect('/login')

    try:
        user = models.users.objects.get(username=req.session['user'])
        liked = json.loads(user.likes or '[]')  # handle None or empty
        
        if str(Id) not in liked:
            liked.append(str(Id))
            user.likes = json.dumps(liked)
            user.save()
            
        return redirect('/like')

    except models.users.DoesNotExist:
        return redirect('/login')

def addremoveitem(request, Id):
    if request.method == 'POST':
        username = request.session.get('user')
        if not username:
            return redirect('/login')

        user = models.users.objects.get(username=username)

        likeitems = json.loads(user.likes) if user.likes else []

        try:
            likeitems.remove(Id)
        except ValueError:
            pass  # item was not in list, ignore

        user.likes = json.dumps(likeitems)
        user.save()

    return redirect('/like')

def like(req):
    if 'user' not in req.session:
        return redirect('/homepage')
    
    username = req.session['user']
    try:
        user = users.objects.get(username=username)

        try:
            liked_ids = json.loads(user.likes)  # convert string to list
        except json.JSONDecodeError:
            liked_ids = []

        liked_items = recipes.objects.filter(id__in=liked_ids)
        return render(req, 'like.html', context={'data': liked_items})
    except users.DoesNotExist:
        return redirect('/login')

def addbuyitem(req, Id):
    if 'user' not in req.session:
        return redirect('/login')

    qty = req.POST.get('qty')

    username = req.session['user']
    user = models.users.objects.get(username=username)

    # Load existing cart
    try:
        cartitems = json.loads(user.cart)
    except (TypeError, json.JSONDecodeError):
        cartitems = []

    new_cart = []
    for item in cartitems:
        if isinstance(item, int):

            new_cart.append({"id": item, "qty": 1})
        else:
            new_cart.append(item)

    # Check if item already exists with same size
    found = False
    for item in new_cart:
        if item["id"] == Id :
            item["qty"] = str(int(item["qty"]) + int(qty))
            found = True
            break

    if not found:
        new_cart.append({
            "id": Id,
            "qty": qty
        })

    user.cart = json.dumps(new_cart)
    user.save()
    return redirect('/carts')

def carts(req):
    if 'user' not in req.session:
        return redirect('/homepage')

    username = req.session['user']
    try:
        user = models.users.objects.get(username=username)
        try:
            cart_data = json.loads(user.cart)
        except json.JSONDecodeError:
            cart_data = []

        cart_items = []
        for item in cart_data:
            try:
                product = models.recipes.objects.get(id=item["id"])
                cart_items.append({
                    "product": product,
                    "qty": item.get("qty", 1)
                })
            except models.recipes.DoesNotExist:
                continue

        return render(req, 'carts.html', context={'data': cart_items})
    except models.users.DoesNotExist:
        return redirect('/login')
    

def searchfood(req,item):
    v = recipes.objects.all().values()
    filterdb = []
    for i in v:
        if i['foodname'].lower().find(item) != -1:
                 filterdb.append(i)
    return render(req, 'searchfood.html', context={"data": filterdb})

def about(req):
    return render(req,'about.html')

def support(req):
    return render(req,'support.html')

def terms(req):
    return render(req,'terms.html')

def privacy(req):
    return render(req,'privacy.html')
