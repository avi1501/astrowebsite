from . import views
from django.urls import path

app_name='basic'

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("services/", views.services, name="services"),
    path("vedic/", views.vedic, name="vedic"),
    path("vastu/", views.vastu, name="vastu"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path('add/<int:product_id>/', views.cart_add, name="cart_add"),
    path("remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("paytmcheckout/", views.paytmcheckout, name="paytmcheckout"),
    path("paypalcheckout/", views.paypalcheckout, name="paypalcheckout"),
    path("paymentsuccess/", views.success, name="success"),
    path("paytmsuccess/", views.paytmsuccess, name="paytmsuccess"),
    path("success/", views.success_url, name="paymentdone"),
    path("handlerequest/", views.handlerequest, name="handlepayment"),
    path("handler/", views.handler, name="handler"),
    


    
   




]
