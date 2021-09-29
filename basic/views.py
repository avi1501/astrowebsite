from django.shortcuts import render, HttpResponse
from . import models
from .forms import ContactForm
import json
from decimal import Decimal
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

def home(request):
    banners = models.Banner.objects.all()
    services = models.Service.objects.all()[:3]
    about = models.About.objects.first()
    context = {
        'banners':banners,
        'services':services,
        'about':about,
    }
    return render(request, "home.html", context)


def about(request):
    about = models.About.objects.first()
    context = {
        "about":about,

    }
    return render(request, "about.html", context)

def services(request):
    services = models.Service.objects.all()
 

    context = {
        "services":services,
    }
    return render(request, "services.html", context)


def contact(request):
    msg = ""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["firstname"]
            last_name = form.cleaned_data["lastname"]
            subject="forms using django"
            message=f"hey {first_name} {last_name} we will get back to you soon"
            reciever = form.cleaned_data['email']
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [reciever, ]
            send_mail( subject, message, email_from, recipient_list )
            msg = "we got your message we will get back to you soon"
            form.save()
            print(f"mail sent to {reciever}")
            
    form = ContactForm()
    context = {
        'form':form,
        "msg":msg,
            }
    return render(request, "contact.html", context)

def vedic(request):
    vedic = models.VedicAstrology.objects.all()
    context = {
        "vedas":vedic,
    }
    return render(request, "vedic-astrology.html", context)


def vastu(request):
    vastu = models.Vastu.objects.all()
    context = {
        "vastus":vastu,
    }
    return render(request, "vastu.html", context)




#cartttttttttttttttttttttttttttttt
from .cart import Cart
import uuid
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

def cart_detail(request, messages=None):
    cart=Cart(request)
    if messages != None:
        messages.success(request, "Item already in Cart")
    
    context = {
        'cart':cart,

    }
    return render(request, "cart.html", context)

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    service = get_object_or_404(models.Service, id=product_id)
    try:
        cart.add(product=service)
    except:
        messages.success(request, "Item Already in Cart")
    return redirect("basic:cart_detail")

@require_POST    
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(models.Service, id=product_id)
    cart.remove(product)
    return redirect("basic:cart_detail")

@require_POST
def paypalcheckout(request):
    cart = Cart(request)

    context = {
        'cart': cart,
       
    }
    return render(request, 'paypalcheckout.html', context)

def paytmcheckout(request):
    cart = Cart(request)
    context = {
        'cart':cart,
    }
    return render(request, 'paytmcheckout.html', context)

@require_POST
def success(request):

    element = request.POST
    firstname = element['firstName']
    
    lastname = element['lastName']
    email = element['email']
    
    phone = element['contactNo']
    address = element['address']
    code = element['code']
    state = element['state']
    country = element['country']
    name = request.session['name'] = firstname+" "+lastname
    email = request.session['email'] = email
    request.session['phone'] = phone
    request.session['address'] = address+" "+ state
    request.session['code'] = code
    request.session['country'] = country
    
    cart = Cart(request)
    
   
    amount = cart.get_total_price_outsider()
    
    # order = models.Order()
    # order.save()
    # x= uuid.uuid4().hex
    
    
    # request.session['tr'] = x
    
    # order.order_id = x
    # order.name = firstname+" "+lastname
    # order.email = email
    # order.IndianClient = False
    # order.InternationalClient = True
    
    # order.countrycode = str(code)
    
    # order.country = country
    # order.contact_no = phone
    
    # order.address = address+" "+state
    
    # for item in cart:
    #     print(item['product'])
    #     order.service_requested.add(item['product'])
    
    # order.amount_paid = cart.get_total_price_outsider()
    # order.save()
    
    context = {
        'cart':cart,
        'name':name,
        'address':address,
        'country':country,
        'phone':phone,
        'email':email,
        'amount':amount,
    }
    return render(request, 'paypalpaymentpage.html', context)


def success_url(request):
    cart = Cart(request)
    name = request.session['name']
    email = request.session['email']
    order = models.Order()
    order.save()
    order.order_id = uuid.uuid4().hex
    order.name = name
    order.email = request.session['email']
    order.IndianClient = False
    order.InternationalClient = True
    
    order.countrycode = request.session['code']
    
    order.country = request.session['country']
    order.contact_no = request.session['phone']
    
    order.address = request.session['address']
    order.payment_status=True



    order_id = order.order_id
    message = f"Hi {name}, your order is successfully done your Order Id is {order_id}. We will contact you soon."
    email_from = settings.EMAIL_HOST_USER
    reciever = email
    subject = f"Order Successfully Placed"
    recipient_list = [reciever, ]
    send_mail(subject, message, email_from, recipient_list)

    for item in cart:
        print(item['product'])
        order.service_requested.add(item['product'])
    
    order.amount_paid = cart.get_total_price_outsider()
    order.save()
    cart.clear()
    del request.session['name']
    # del request.session['email']
    # del request.session['code']
    # del request.session['country']
    # del request.session['phone']
    # del request.session['address']
    context = {
        'order_id':order_id,
    }
    
    return render(request, "paymentSuccess.html", context)



@require_POST
def paytmsuccess(request):

    element = request.POST
    firstname = element['firstName']
    
    lastname = element['lastName']
    email = element['email']
    
    phone = element['contactNo']
    address = element['address']
    code = element['code']
    state = element['state']
    country = element['country']
    name = request.session['name'] = firstname+" "+lastname
    email = request.session['email'] = email
    request.session['phone'] = phone
    request.session['address'] = address+" "+ state
    request.session['code'] = code
    request.session['country'] = country
    
    cart = Cart(request)
    
   
    amount = cart.get_total_price_outsider()
    
    # order = models.Order()
    # order.save()
    # x= uuid.uuid4().hex
    
    
    # request.session['tr'] = x
    
    # order.order_id = x
    # order.name = firstname+" "+lastname
    # order.email = email
    # order.IndianClient = False
    # order.InternationalClient = True
    
    # order.countrycode = str(code)
    
    # order.country = country
    # order.contact_no = phone
    
    # order.address = address+" "+state
    
    # for item in cart:
    #     print(item['product'])
    #     order.service_requested.add(item['product'])
    
    # order.amount_paid = cart.get_total_price_outsider()
    # order.save()
    request.session['order_id'] = str(uuid.uuid4().hex)
    amount = cart.get_total_price_outsider()
    merchent_id = "jXVIMO88695068103329"
    merchent_key = "Vy4IOSdz10%ifr0y"
    print(request.session['order_id'])
    param_dict = {
        "MID": merchent_id,
        "ORDER_ID": request.session['order_id'],
        "CUST_ID": email,
        "TXN_AMOUNT": str(amount),
        "CHANNEL_ID": "WEB",
        "INDUSTRY_TYPE_ID": "Retail",
        "WEBSITE": "WEBSTAGING",
        'CALLBACK_URL':'http://localhost:8000/handlerequest/',
    }
    from . import checksum
    param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict,merchent_key)
    context = {
        'param_dict':param_dict,
    }
    
    return render(request, 'paytmpaymentpage.html', context)

@require_POST
def failure(request):
    element = request.POST
    return HttpResponse("failure")

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def handlerequest(request):
    return render(request, "handler.html")

@require_POST
def handler(request):
    cart = Cart(request)
    order_id = request.session['order_id']
    name = request.session['name']
    email = request.session['email']
    order = models.Order()
    order.save()
    order.order_id = order_id
    order.name = name
    order.email = request.session['email']
    order.IndianClient = True
    order.InternationalClient = False
    
    order.countrycode = request.session['code']
    
    order.country = request.session['country']
    order.contact_no = request.session['phone']
    
    order.address = request.session['address']
    order.payment_status=True



    order_id = order.order_id
    message = f"Hi {name}, your order is successfully done your Order Id is {order_id}. We will contact you soon."
    email_from = settings.EMAIL_HOST_USER
    reciever = email
    subject = f"Order Successfully Placed"
    recipient_list = [reciever, ]
    send_mail(subject, message, email_from, recipient_list)

    for item in cart:
        print(item['product'])
        order.service_requested.add(item['product'])
    
    order.amount_paid = cart.get_total_price_local()
    order.save()
    cart.clear()
    del request.session['name']
    # del request.session['email']
    # del request.session['code']
    # del request.session['country']
    # del request.session['phone']
    # del request.session['address']
    context = {
        'order_id':order_id,
    }
    
    return render(request, "paymentSuccess.html", context)
