from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import *
from django.http import JsonResponse
import json
from .forms import CommentForm,AddProductForm
from .forms import UserChangeForm,EditProfileform
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm,PasswordResetForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
import datetime
from .utils import cookieCart,cartData,guestUser
from django.db.models import Q
from django.views.generic import CreateView
# Create your views here.

def search(request):
    try:
        q=request.GET.get('q')
        print(q)
    except:
        q=None
    data = cartData(request)
    cartItems = data['cartItems']
    if q:
        queryset=(Q(name__icontains=q))
        products = Product.objects.filter(queryset).distinct()
        if products:
            print("q is in products")
            context={'query':q,'products':products,'cartItems':cartItems}
            template = "store/search.html"
        else:
            print("q is NOT in products")
            message="No match found for :"
            products = Product.objects.all()
            context = {'query': q, 'products': products,'message':message,'cartItems':cartItems}
            template = "store/search.html"

    else:
        print("no q")
        products = Product.objects.all()
        template = "store/search.html"
        context = {'products':products,'cartItems':cartItems}
    return render(request, template,context)


def index(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products=Product.objects.all()
    context={'products':products,'cartItems':cartItems}
    return render(request,"store/index.html",context)

def login_view(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "store/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "store/login.html",{'cartItems':cartItems})

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]
        birth_date=request.POST["birth_date"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        #avatar=request.POST["avatar"]
        if password != confirmation:
            return render(request, "store/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = Customer.objects.create_user(username,email, password,first_name=first_name,last_name=last_name,
                                            phone_number=phone_number,birth_date=birth_date)
            user.save()
        except IntegrityError:
            return render(request, "store/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "store/register.html",{'cartItems':cartItems})

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order,'cartItems':cartItems}
    return render(request,'store/cart.html',context)
@login_required
def view_profile(request):
    data = cartData(request)
    cartItems = data['cartItems']
    args={'user':request.user}
    return render(request,"store/profile.html",{'cartItems':cartItems})

@login_required
def edit_profile(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if request.method=='POST':
        form=EditProfileform(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("/store/profile")
    else:
        form=EditProfileform(instance=request.user)
        args={'form':form,'cartItems':cartItems}
        return render(request,'store/edit_profile.html',args)
@login_required
def resetpassword(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if request.method=='POST':
        form=PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect("/store/profile")
        else:
            return redirect('/store/profile/resetpassword',{'cartItems':cartItems})
    else:
        form=PasswordChangeForm(user=request.user)
        args={'form':form,'cartItems':cartItems}
        return render(request,'store/resetpassword.html',args)
@login_required
def add_product(request):
    data = cartData(request)
    cartItems = data['cartItems']
    print(cartItems)
    products=Product.objects.all()
    context={'products':products}
    if request.method=='POST':
        form=AddProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/store/add_product")
    else:
        form=AddProductForm()
        return render(request,'store/add_product.html',{'form':form,'context':context,'cartItems':cartItems})
def checkout(request):
    data=cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order,'cartItems':cartItems}
    return render(request,'store/checkout.html',context)

def update_item(request):
    data = json.loads(request.body)
    productId=data['productId']
    action=data['action']
    print('Action:',action)
    print('productId:',productId)

    purchaser = request.user.purchaser
    product=Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=purchaser, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        purchaser = request.user.purchaser
        order, created = Order.objects.get_or_create(customer=purchaser, complete=False)
    else:
        customer, order = guestUser(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()


    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=purchaser,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)

def view_product(request,id):
    data = cartData(request)
    cartItems = data['cartItems']
    product=Product.objects.get(id=id)
    comments = product.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product
            new_comment.save()
    else:
        comment_form = CommentForm()
    context = {'product': product, 'cartItems': cartItems, 'comment_form': comment_form, 'new_comment': new_comment,
               'comments': comments}
    return render(request,'store/view_product.html',context)


def categories(request):
    if request.method == "GET":
        category = Product.objects.all()
        all_categories = []
        for i in category:
            if i.category != None:
                all_categories.append(i.category)

        print(all_categories)
        return render(request,'store/categories.html', {
            'categories': all_categories,
        })
def categorypage(request,category):
    products=Product.objects.filter(category=category)
    return render(request, 'auctions/categoryPage.html', {
        "products":products,
        "category": category,
    })
def aboutUs(request):
    data = cartData(request)
    cartItems = data['cartItems']
    return render(request, 'store/aboutus.html',{'cartItems':cartItems})
def contactUs(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if request.method == "POST":
        FirstName = request.POST["FirstName"]
        LastName = request.POST["LastName"]
        City = request.POST["City"]
        Subject= request.POST["Subject"]
        feedback = Feedback.objects.create(FirstName=FirstName,LastName=LastName,City=City,Subject=Subject)

        feedback.save()
    return render(request, 'store/contactus.html',{'cartItems':cartItems})


