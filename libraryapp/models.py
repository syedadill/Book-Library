from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='favorited_by', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'book')
            