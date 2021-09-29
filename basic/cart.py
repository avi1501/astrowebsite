from django.conf import settings
from basic.models import Service
from decimal import Decimal

class Cart(object):
    def __init__(self, request):
        """Initializing cart """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'price_local':str(product.price_local), 'price_outsider':str(product.price_outsider)}
        else:
            raise ValueError("already added")
        self.save()
    
    def save(self):
        self.session.modified = True
    
    def remove(self, product):
        product_id = str(product.id)
        print(self.cart)
     
        if product_id in self.cart:
            del self.cart[str(product.id)]
            self.save()
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Service.objects.filter(id__in = product_ids)

        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price_local'] = Decimal(item['price_local'])
            item['price_outsider'] = Decimal(item['price_outsider'])
            
            yield item
    
    
    def get_total_price_local(self):
        return sum([Decimal(item['price_local']) for item in self.cart.values()])

    def get_total_price_outsider(self):
        return sum([Decimal(item['price_outsider']) for item in self.cart.values()])

    def get_item_no(self):
        return len(self.cart)

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
    