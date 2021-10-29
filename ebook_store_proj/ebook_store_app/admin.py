from django.contrib import admin
from .models import *


admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(BookRating)
admin.site.register(Shipping)
