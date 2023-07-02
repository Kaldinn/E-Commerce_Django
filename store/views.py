from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

import json
import datetime

from .utils import cookie_cart, cart_data, guest_order
from .models import *
from .forms import CreateUserForm

def view_product(request, pk):
    data = cart_data(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']
        
    product = get_object_or_404(Product, id=pk)
    context = {'product':product, 'items':items, 'order': order, 'cart_items': cart_items}
    return render(request, 'store/view.html', context)


# Create your views here.
def store(request):
    data = cart_data(request)

    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cart_items': cart_items}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cart_data(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']
        
    context = {'items':items, 'order': order, 'cart_items': cart_items}
    return render(request, 'store/cart.html', context) 


def checkout(request):

    data = cart_data(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order': order, 'cart_items': cart_items}
    return render(request, 'store/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action: ', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('item was added', safe=False)
    

def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        

    else:
        customer, order = guest_order(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id 

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAdress.objects.create(
            customer=customer,
            order=order,
            adress=data['shipping']['adress'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'] 
        )

    return JsonResponse('Payment Complete', safe=False)



# def login_page(request):
#     data = cart_data(request)
#     cart_items = data['cart_items']
#     order = data['order']
#     items = data['items']

#     form = CreateUserForm()

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             print("good")
#             return redirect('store')


#     context = {'form': form, 'items':items, 'order': order, 'cart_items': cart_items}
#     return render(request, 'store/login.html', context)

# def logout_user(request):
#     logout(request)
#     return redirect('login')


# def register_page(request):
#     data = cart_data(request)
#     cart_items = data['cart_items']
#     order = data['order']
#     items = data['items']

#     form = CreateUserForm()

#     if request.method == 'POST':
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             user = form.cleaned_data.get('username')
#             user = User.objects.get(username=user)
#             customer = Customer.objects.create(user=user, email=form.cleaned_data['email'])

#             messages.success(request, f"Account was created for {user}")
#             return redirect('login')

#     context = {'form': form, 'items':items, 'order': order, 'cart_items': cart_items}
#     return render(request, 'store/register.html', context)