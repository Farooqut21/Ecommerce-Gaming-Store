import json
from .models import *
from django.core.exceptions import ObjectDoesNotExist

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']
    for i in cart:
        try:
            cartItems += cart[i]["quantity"]
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'Imagecheck': product.Imagecheck,
                },
                'quantity': cart[i]["quantity"],
                'get_total': total,
            }
            items.append(item)
            if product.digital == False:
                order['shipping'] == True

        except:
            pass
    return {'cartItems':cartItems,'order':order,'items':items}

def cartData(request):

    if request.user.is_authenticated:
        print(request.user.email,request.user.username)
        try:
            customer = request.user.purchaser
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        except ObjectDoesNotExist:
            purchaser, created = Purchaser.objects.get_or_create(
                user=request.user,
                email=request.user.email,
                name = request.user.username,
            )
            purchaser.save()
            customer = request.user.purchaser
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems':cartItems,'order':order,'items':items}


def guestUser(request,data):
    print("User is not logged in.")
    print("COOKIES:", request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']
    purchaser, created = Purchaser.objects.get_or_create(
        email=email,
    )
    purchaser.name = name
    purchaser.save()
    order = Order.objects.create(
        customer=purchaser, complete=False
    )
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )


    return purchaser,order