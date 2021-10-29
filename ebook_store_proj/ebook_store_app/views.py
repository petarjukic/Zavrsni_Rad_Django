from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.http import HttpResponseRedirect, JsonResponse

import json, datetime, stripe

from django.core.paginator import Paginator, EmptyPage

from django.urls import reverse, reverse_lazy

from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import *
from .models import *
from .filters import BookFilter
from .utils import cart_data, guest_order, UserAccess



def register_user(request):
    if request.user.is_authenticated:
        return redirect('ebook_store_app:home')

    form = CreateUserForm()

    if request.method == 'POST':
        if UserProfile.objects.filter(email=request.POST['email']).exists():
            old_user = UserProfile.objects.get(email=request.POST['email'], password="")
            old_user.set_password(request.POST['password1'])
            old_user.name = request.POST['name']
            old_user.save()
            return redirect('login_user')
        else:
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                return redirect('login_user')

    context = {'form':form}
    return render(request, './account/register.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('ebook_store_app:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('ebook_store_app:home')
        else:
            messages.info(request, 'USERNAME OR PASSWORD IS INCORRECT!!')

    return render(request, "./account/login.html", {})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('ebook_store_app:home'))


class UserListView(UserAccess, ListView):
    model = UserProfile
    context_object_name = 'users'
    template_name = 'account/user-view.html'


class UpdateUserView(UserAccess, UpdateView):
    model = UserProfile
    template_name = 'account/update-user.html'
    fields = ['username', 'email', 'status']
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('ebook_store_app:user-view')


class DeleteUserView(UserAccess, DeleteView):
    model = UserProfile
    pk_url_kwarg = 'pk'
    template_name = 'account/delete-user.html'
    success_url = reverse_lazy('ebook_store_app:user-view')


def book_view(request):
    genres = Genre.objects.all()
    books = Book.objects.all()
    data = cart_data(request)
    cart_items = data['cart_items']
    my_filter = BookFilter(request.GET, queryset=books)
    books = my_filter.qs
    my_page = Paginator(books, 8)
    page_number = request.GET.get('page', False)
    all_pages = my_page.num_pages

    try:
        books = my_page.page(page_number)
    except EmptyPage:
        books = my_page.page(1)

    context = {'books':books, 'genres':genres , 'cart_items':cart_items, 'my_filter':my_filter, 'all_pages':all_pages}

    return render(request, './home/home.html', context)
    

def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    related_books = Book.objects.filter(genre_id=book.genre_id).exclude(id=book_id)
    data = cart_data(request)
    cart_items = data['cart_items']
    
    context = {'book':book, 'related_books':related_books, 'cart_items':cart_items}
    return render(request, './home/book-detail.html', context)


class AddBookView(UserAccess, CreateView):
    model = Book
    form_class = AddBookForm
    template_name = 'actions/add-book.html'
    success_url = reverse_lazy('ebook_store_app:home')


class UpdateBookView(UserAccess, UpdateView):
    model = Book
    template_name = 'actions/update-book.html'
    fields = '__all__'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('ebook_store_app:home')


class DeleteBookView(UserAccess, DeleteView):
    model = Book
    pk_url_kwarg = 'pk'
    template_name = 'actions/delete-book.html'
    success_url = reverse_lazy('ebook_store_app:home')


def about_view(request):
    data = cart_data(request)
    cart_items = data['cart_items']
    return render(request, './info/about.html', {'cart_items':cart_items})


class AuthorListView(ListView):
    model = Author
    context_object_name = "authors"
    template_name = 'author/author-view.html'


class AddAuthorView(UserAccess, CreateView):
    model = Author
    fields = '__all__'
    template_name = 'author/add-author.html'
    success_url = reverse_lazy('ebook_store_app:author-view')


class UpdateAuthorView(UserAccess, UpdateView):
    model = Author
    template_name = 'author/update-author.html'
    fields = '__all__'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('ebook_store_app:author-view')


class DeleteAuthorView(UserAccess, DeleteView):
    model = Author
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('ebook_store_app:author-view')
    template_name = 'author/delete-author.html'


class GenreListView(ListView):
    model = Genre
    context_object_name = "genres"
    template_name = 'genre/genre-view.html'


class AddGenreView(UserAccess, CreateView):
    model = Genre
    fields = '__all__'
    template_name = 'genre/add-genre.html'
    success_url = reverse_lazy('ebook_store_app:genre-view')


class UpdateGenreView(UserAccess, UpdateView):
    model = Genre
    template_name = 'genre/update-genre.html'
    fields = '__all__'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('ebook_store_app:genre-view')


class DeleteGenreView(UserAccess, DeleteView):
    model = Genre
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('ebook_store_app:genre-view') 
    template_name = 'genre/delete-genre.html'


class PublisherListView(ListView):
    model = Publisher
    context_object_name = "publishers"
    template_name = 'publisher/publisher-view.html'


class AddPublisherView(UserAccess, CreateView):
    model = Publisher
    fields = '__all__'
    template_name = 'publisher/add-publisher.html'
    success_url = reverse_lazy('ebook_store_app:publisher-view')


class UpdatePublisherView(UserAccess, UpdateView):
    model = Publisher
    template_name = 'publisher/update-publisher.html'
    fields = '__all__'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('ebook_store_app:publisher-view')


class DeletePublisherView(UserAccess, DeleteView):
    model = Publisher
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('ebook_store_app:publisher-view') 
    template_name = 'publisher/delete-publisher.html'


def cart(request):
    data = cart_data(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']

    context = {'items':items, 'order':order, 'cart_items':cart_items}
    return render(request, './home/cart.html', context)


def checkout(request):
    data = cart_data(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']

    context = {'items':items, 'order':order, 'cart_items':cart_items}
    return render(request, './home/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Book.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer_id=customer, complete=False) 
    orderItem, created = OrderDetails.objects.get_or_create(order_id=order, book_id=product)

    if action == 'add':
        orderItem.total = (orderItem.total + 1)
    elif action == 'remove':
        orderItem.total = (orderItem.total - 1)

    orderItem.save()

    if orderItem.total <= 0:
        orderItem.delete()

    return JsonResponse('Item added', safe=False)


def process_order(request):
    number = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer_id=customer, complete=False) 

    else:
        customer, order = guest_order(request, data)

    total = float(data['form']['total'])
    order.order_number = number

    if total == float(order.get_cart_total):
        order.complete = True 
            
    order.save()
    Shipping.objects.create(
        customer_id=customer,
        order_id=order,
        adress=data['shipping']['adress'],
        city=data['shipping']['city'],
        country=data['shipping']['country'],
        zip_code=data['shipping']['zip_code'],
    )

    return JsonResponse("Order completed", safe=False)

def payment(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        order_user = Order.objects.filter(payed=False, complete=True).first() 
        user = order_user.customer_id
    
    order = Order.objects.filter(customer_id=user, payed=False, complete=True).first()
    
    if request.method == 'POST':
        order.payed = True
        order.save()
        
        customer = stripe.Customer.create(
            email=user.email,
            name=user.username,
            source=request.POST['stripeToken']
        )
        charge = stripe.Charge.create(
            customer=customer,
            amount=int(order.get_cart_total * 100),
            currency='usd',
            description='Charge for buying book/s'
        )
        return redirect(reverse('ebook_store_app:home'))
        
    return render(request, './home/payment.html', {})


@login_required
def book_rate(request, book_id):
    user = request.user
    book = Book.objects.get(id=book_id)
    mark = request.POST['rate']
    
    if(BookRating.objects.filter(customer_id=user, book_id=book)):
        rated = BookRating.objects.get(customer_id=user, book_id=book) 
        rated.rate = mark
        rated.save()
    else:
        rate = BookRating.objects.create(customer_id=user, book_id=book, rate=mark) 
        rate.save()

    return redirect(reverse('ebook_store_app:home'))  


class OrderListView(UserAccess, ListView):
    model = OrderDetails
    context_object_name = "orders"
    template_name = 'info/order-view.html'


def best_sellers(request):
    data = cart_data(request)
    cart_items = data['cart_items']
    books = Book.objects.all()
    best_seller_book = []
    best_seller_dict = {}

    for book in books:
        number_of_books = 0
        order_details = OrderDetails.objects.filter(book_id=book)
        for order in order_details:
            number_of_books += order.total
        
        order_details = OrderDetails.objects.filter(book_id=book).first()
        best_seller_dict[order_details] = number_of_books

    sorted_items = sorted(best_seller_dict.items(), key=lambda x: x[1], reverse=True)

    for i in range(0, 5):
        best_seller_book.append(sorted_items[i][0])

    context = {'cart_items':cart_items, 'best_seller_book':best_seller_book}
    return render(request, './info/best-sellers.html', context)


def best_sellers_genre(request, genre_id):
    data = cart_data(request)
    cart_items = data['cart_items']
    books = Book.objects.filter(genre_id=genre_id)
    best_seller_book = []
    best_seller_dict = {}
    number = 0
    
    for book in books:
        number_of_books = 0
        order_details = OrderDetails.objects.filter(book_id=book, book_id__genre_id=genre_id)
        
        if len(order_details) > 0:
            number +=  1
        
        for order in order_details:
            number_of_books += order.total

        order_details = OrderDetails.objects.filter(book_id=book, book_id__genre_id=genre_id).first()
        best_seller_dict[order_details] = number_of_books

    sorted_items = sorted(best_seller_dict.items(), key=lambda x: x[1], reverse=True)

    if number > 5:
        number = 5

    for i in range(0, number):
        best_seller_book.append(sorted_items[i][0])

    context = {'cart_items':cart_items, 'best_seller_book':best_seller_book}
    return render(request, './info/best-sellers-genre.html', context)
