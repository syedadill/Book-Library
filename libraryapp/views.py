from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User 


@api_view(['GET', 'POST'])
def book_list(request):
    if request.method == 'GET':
        search_query = request.GET.get('search', '')
        books = Book.objects.filter(Q(title__icontains=search_query) | Q(author__name__icontains=search_query))
        serializers = BookSerializer(books, many=True)
        return Response(serializers.data)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication Required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializers = BookSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)    
@api_view(['GET','PUT', 'DELETE'])
def book_details(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({'detail': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method =='GET':
        serializers= BookSerializer(book)
        return Response(serializers.data)

    if request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        serializers = BookSerializer(book, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        if not request.user.is_authenticated:
           return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        Author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def favorite_book(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response({'detail': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'POST':
        # Add book to favorites
        Favorite.objects.get_or_create(user=request.user, book=book)
        return Response({'detail': 'Book added to favorites'}, status=status.HTTP_201_CREATED)
    
    if request.method == 'DELETE':
        # Remove book from favorites
        favorite = Favorite.objects.filter(user=request.user, book=book)
        favorite.delete()
        return Response({'detail': 'Book removed from favorites'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommended_books(request):
    user_favorites = Favorite.objects.filter(user=request.user)
    if not user_favorites.exists():
        return Response({'detail': 'No favorites found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Implement a similarity-based recommendation logic here.
    # For simplicity, just returning random books for now.
    recommended_books = Book.objects.exclude(favorited_by__user=request.user)[:5]
    serializer = BookSerializer(recommended_books, many=True)
    return Response(serializer.data)

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if User.objects.filter(username=username).exists():
        return Response({'detail': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, password=password)
    return Response({'detail': 'User created successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.filter(username=username).first()
    
    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
