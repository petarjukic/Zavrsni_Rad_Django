from django.urls import path
from ebook_store_app import views


app_name = 'ebook_store_app'

urlpatterns = [
    path('home/', views.book_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('user-view/', views.UserListView.as_view(), name='user-view'),
    path('update-user/<int:pk>/', views.UpdateUserView.as_view(), name='update-user'),
    path('delete-user/<int:pk>/', views.DeleteUserView.as_view(), name='delete-user'),
    
    path('add-book/', views.AddBookView.as_view(), name='add-book'),
    path('update-book/<int:pk>/', views.UpdateBookView.as_view(), name='update-book'),
    path('delete-book/<int:pk>/', views.DeleteBookView.as_view(), name='delete-book'),
    path('detail-book/<int:book_id>/', views.book_detail, name='detail-book'),

    path('add-author/', views.AddAuthorView.as_view(), name='add-author'),
    path('delete-author/<int:pk>/', views.DeleteAuthorView.as_view(), name='delete-author'),
    path('update-author/<int:pk>/', views.UpdateAuthorView.as_view(), name='update-author'),
    path('author-view/', views.AuthorListView.as_view(), name='author-view'),

    path('add-genre/', views.AddGenreView.as_view(), name='add-genre'),
    path('delete-genre/<int:pk>/', views.DeleteGenreView.as_view(), name='delete-genre'),
    path('update-genre/<int:pk>/', views.UpdateGenreView.as_view(), name='update-genre'),
    path('genre-view/', views.GenreListView.as_view(), name='genre-view'),

    path('add-publisher/', views.AddPublisherView.as_view(), name='add-publisher'),
    path('delete-publisher/<int:pk>/', views.DeletePublisherView.as_view(), name='delete-publisher'),
    path('update-publisher/<int:pk>/', views.UpdatePublisherView.as_view(), name='update-publisher'),
    path('publisher-view/', views.PublisherListView.as_view(), name='publisher-view'),

    path('update-item/', views.update_item, name='update_item'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('process-order/', views.process_order, name='process_order'),

    path('payment/', views.payment, name='payment'),
    path('book-rate/<int:book_id>/', views.book_rate, name='book_rate'),
    path('order-view/', views.OrderListView.as_view(), name='order-view'),
    path('best-sellers/', views.best_sellers, name='best-sellers'),
    path('best-sellers/<int:genre_id>/', views.best_sellers_genre, name='best-sellers-genre'),
]