from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Book

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = [ 'id', 'title', 'content', 'subtitle', 'author', 'isbn', 'price']


    def validate(self, data):
        title = data.get('title', None)
        author = data.get('author', None)
        print(data)

    
        # Check title and author from database existence
        if Book.objects.filter(title=title, author=author).exists():
            raise ValidationError(
                {
                    'status' : False,
                    'massage' : "Unique error"
                }
            )
        return data
    

    def validate_price(self, price):
        if price < 0 or price > 999999999:
            raise ValidationError(
                {
                    "status":False
                }
            ) 
        return price


class BookApiViewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, max_length=200)
    subtitle = serializers.CharField(required=True, max_length=200)
    content = serializers.CharField(required=True)
    author = serializers.CharField(required=True, max_length=100)
    isbn = serializers.CharField(required=True, max_length=13)
    price= serializers.DecimalField(required=True, decimal_places=2, max_digits=20)


    def create(self, validated_data):
        return Book.objects.create(**validated_data)