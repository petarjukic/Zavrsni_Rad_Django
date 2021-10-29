import json
from .models import *
from django.views.generic import View
from django.contrib.auth.mixins import AccessMixin


def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_cart_total':0, 'get_cart_items':0}
    cart_items = order['get_cart_items']

    for cart_product in cart:
        try:
            cart_items += cart[cart_product]["quantity"]
            product = Book.objects.get(id=cart_product)
            total = (product.price * cart[cart_product]["quantity"])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[cart_product]["quantity"]

            item = {
                'book_id':{
                    'id':product.id, 'title':product.title, 'description':product.description,
                    'picture':product.picture, 'price':product.price,              'publication_year':product.publication_year, 'author_id':product.author_id,
                    'publisher_id':product.publisher_id, 'genre_id':product.genre_id,
                },
                'quantity':cart[cart_product]["quantity"],
                'get_total':total
            }
            items.append(item)
        except:
            pass
    return {'items':items, 'order':order, 'cart_items':cart_items}


def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer_id=customer, complete=False)
        items = order.orderdetails_set.all()
        cart_items = order.get_cart_items
    else:
        cookie_data = cookie_cart(request)
        items = cookie_data['items']
        order = cookie_data['order']
        cart_items = cookie_data['cart_items']

    return {'items':items, 'order':order, 'cart_items':cart_items}


def guest_order(request, data):
    username = data['form']['username']
    email = data['form']['email']
    cookie_data = cookie_cart(request)
    items = cookie_data['items']

    customer, created = UserProfile.objects.get_or_create(
        email=email,
    )
    customer.username = username
    customer.save()

    order = Order.objects.create(
        customer_id=customer,
        complete=False,
    )
    
    for item in items:
        product = Book.objects.get(id=item['book_id']['id'])

        order_detail = OrderDetails.objects.create(
            book_id=product,
            order_id=order,
            total=item['quantity']
        )
    return customer, order


class UserAccess(AccessMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.request.user.status == 'Admin':
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
