from django.db import models

from django.utils.safestring import mark_safe
# Create your models here.

class Banner(models.Model):
    img = models.ImageField(upload_to="banners/")
    alt_text = models.CharField(max_length=150)

    def __str__(self):
        return self.alt_text
    
    def img_tag(self):
        return mark_safe('<img src = "%s" width="80"/>'%(self.img.url))


class VedicAstrology(models.Model):
    heading = models.CharField(max_length=1000)
    smalldesc = models.CharField(max_length=1000)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.heading
    
    class Meta:
        ordering = ['-date_created']

class Vastu(models.Model):
    heading = models.CharField(max_length=1000)
    smalldesc = models.CharField(max_length=1000)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.heading

    class Meta:
        ordering = ['-date_created']

class Contact(models.Model):
    firstname = models.CharField(max_length=10)
    lastname = models.CharField(max_length=10) 
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=100)

    def __str__(self):
        return self.email

class Service(models.Model):
    img = models.ImageField(upload_to="services/", null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price_local = models.FloatField()
    price_outsider = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title
    
    def image_tag(self):
        return mark_safe("<img src='%s' width='80'/>"%(self.img.url))

    class Meta:
        ordering = ['-date_created']


class About(models.Model):
    img = models.ImageField(upload_to="about/", null=True)
    alt_text = models.CharField(max_length=100)
    title = models.CharField(max_length = 100)
    description1 = models.TextField()
    description2 = models.TextField()
    

    def __str__(self):
        return self.title

class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    service_requested = models.ManyToManyField("Service")
    amount_paid = models.IntegerField(null=True)
    payment_status = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    IndianClient = models.BooleanField(default=True)
    InternationalClient=models.BooleanField(default=False)
    countrycode = models.CharField(max_length=4)
    contact_no = models.IntegerField(null=True)
    address = models.TextField()
    country = models.CharField(max_length=40)

    def __str__(self):
        return self.email

    def total_amount(self):
        return self.amount_paid
    

    


    


