from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    ADMIN = 'Admin'
    CUSTOMER = 'Customer'
    ROLES = (
        (ADMIN,'Admin'), 
        (CUSTOMER,'Customer'),
    )

    email = models.CharField(max_length=64, unique=True, blank=False)
    name = models.CharField(max_length=64, null=True)
    status = models.CharField(max_length=16, choices=ROLES, default=CUSTOMER)

    def __str__(self):
        return self.email


class Author(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    INDETERMINATE = 'Indeterminate'
    SEXES = (
        (MALE,'Male'), 
        (FEMALE,'Female'),
        (INDETERMINATE, 'Indeterminate')
    )
    first_name = models.CharField(max_length=64, blank=False, null=False)
    last_name = models.CharField(max_length=64, blank=False, null=False)
    age = models.PositiveIntegerField(blank=False, null=False)
    sex = models.CharField(max_length=20, choices=SEXES)

    def __str__(self):
        return ('%s %s') % (self.first_name, self.last_name)


class Publisher(models.Model):
    company_name = models.CharField(max_length=150, blank=False, null=True, unique=True)
    adress = models.CharField(max_length=80, blank=True, null=True)

    def __str__(self):
        return self.company_name


class Genre(models.Model):
    genre_type = models.CharField(max_length=64, null=True, blank=False, unique=True)

    def __str__(self):
        return self.genre_type


class Book(models.Model):
    title = models.CharField(max_length=120, null=False, blank=False, unique=True)
    description = models.TextField()
    picture = models.ImageField(null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    publication_year = models.PositiveIntegerField()
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher_id = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)

    @property
    def get_mean_value(self):
        number_of_rated_books = BookRating.objects.filter(book_id=self.id).count()
        rated_books = BookRating.objects.filter(book_id=self.id)
        rate = sum([rated_book.rate for rated_book in rated_books])
        
        if rate == 0:
            return rate
        mean_value = rate / number_of_rated_books
        return round(mean_value, 2)

    def __str__(self):
        return self.title


class Order(models.Model):
    order_number = models.CharField(max_length=150, null=True, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    payed = models.BooleanField(default=False)
    customer_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    @property
    def get_cart_total(self):
        order_items = self.orderdetails_set.all()
        total_number = sum([item.get_total for item in order_items])
        return total_number

    @property
    def get_cart_items(self):
        order_items = self.orderdetails_set.all()
        total_number = sum([item.total for item in order_items])
        return total_number

    def __str__(self):
        return ('%s, %s') % (str(self.id), self.order_number)
    

class OrderDetails(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    total = models.PositiveIntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total_number = self.book_id.price * self.total
        return total_number

    def __str__(self):
        return str(self.id)


class BookRating(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rate = models.IntegerField(null=True, blank=True)
    rating_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Shipping(models.Model):
    customer_id = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    order_id = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    adress = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    country = models.CharField(max_length=100, null=False)
    zip_code = models.CharField(max_length=100, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ('%s, %s') % (self.adress, self.city)
