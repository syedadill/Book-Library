from django.urls import path
from . import views

urlpatterns = [
    # Book endpoints
    path('books/', views.book_list, name='book-list'),
    path('books/<int:pk>/', views.book_details, name='book-detail'),
    
    # Author endpoints
    

    # Authentication endpoints
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),

    # Favorites and recommendations
    path('books/<int:book_id>/favorite/', views.favorite_book, name='favorite-book'),
    path('books/recommended/', views.recommended_books, name='recommended-books'),
]
