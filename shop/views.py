import json
from django.http import JsonResponse
from django.contrib import auth 
from django.shortcuts import redirect, render
from shop.form import customUserCreationForm
from.models import *
from django.contrib import messages
from django .contrib.auth import authenticate,login
from django .contrib import auth
from django.db.models import Q

# Create your views here.
def home(request):
   products=Product.objects.filter(treading=0)
   return render(request, 'shop/index.html',{"products":products})

def remove_from_cart(request,cid):
  cart_item = Cart.objects.get(id=cid)
  cart_item.delete() 
  return redirect('cart_page')

def search(request):

    query = request.GET.get('q', '').strip()

    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )

    context = {
        "products": products,
        "query": query
    }

    return render(request, "shop/search.html", context)


def search_products(request):

    query = request.GET.get('q', '').strip()

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        products = Product.objects.none()

    data = {
        "products": list(products.values("id", "name"))
    }

    return JsonResponse(data)
   

def cart_page(request):
   cart=None
   if request.user.is_authenticated: 
      cart=Cart.objects.filter(user=request.user)
      return render(request,"shop/cart_page.html",{"cart":cart})
   else:
      return redirect("/")
   
def add_to_cart(request): 
   if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
      if request.user.is_authenticated: 
         data = json.loads(request.body) 
         product_qty = data['product_qty'] 
         product_id = data['pid'] 
         product_status = Product.objects.get(id=product_id) 
         if product_status: 
            if Cart.objects.filter(user=request.user, product_id=product_id).exists(): 
               return JsonResponse({'status':'Product Already in Cart'}, status=200) 
            else: 
               if product_status.quantity >= int(product_qty): 
                  Cart.objects.create( 
                     user=request.user, 
                     product_id=product_id, 
                     product_qty=product_qty
                       ) 
                  return JsonResponse({'status':'Product Added to Cart'}, status=200)  
               else: 
                  return JsonResponse({'status':'Product Stock not Available'}, status=200) 
         else: 
                  return JsonResponse({'status':'Product Not Found'}, status=200) 
      else: 
         return JsonResponse({'status':'Login to add cart'}, status=200) 
   else: 
            return JsonResponse({'status':'Invalid Access'}, status=200)

def logout(request):
    auth.logout(request)
    messages.success(request,"Logout Successfull")
    return redirect('/')

def login(request):
   if request.user.is_authenticated:
      return redirect('home')
   else: 
   
    if request.method=="POST":
      name=request.POST.get('username')
      password=request.POST.get('password')
      user=authenticate(request,username=name,password=password)
      if user is not None:
         login(request,user)
         messages.success(request,"Login Successfull")
         return redirect('home')
      else:
         messages.error(request,"Invalid username or password")
         return redirect('/login')
   return render(request, 'shop/login.html')

def register(request):
   form=customUserCreationForm()
   if request.method=="POST":
      form=customUserCreationForm(request.POST)
      if form.is_valid():
         form.save()
         messages.success(request,"Registration Successfull")
         return redirect('login')
   return render(request, 'shop/register.html',{"form":form})

def collection(request):
   category=Category.objects.filter(status=0)
   return render(request, 'shop/collection.html',{"category":category})

def collectionsview(request,name):
   if(Category.objects.filter(status=0,name=name)):
      products=Product.objects.filter(category__name=name)
      return render(request, 'shop/products/index.html',{"products":products,"category_name":name})
   else:
      messages.warning(request,"No such Category Found")
      return  redirect('collections')
   
def products_ditails(request,cname,pname):
   if(Category.objects.filter(status=0,name=cname)):
      if(Product.objects.filter(name=pname)):
         products=Product.objects.filter(name=pname).first()
         return render(request, 'shop/products/details.html',{"products":products})
      else:
         messages.warning(request,"No such Product Found")
         return  redirect('collections')
   else:
      messages.warning(request,"No such Category Found")
      return  redirect('collections')