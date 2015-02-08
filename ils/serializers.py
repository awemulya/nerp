from rest_framework import serializers
from models import Book, Record, Transaction


class BookSerializer(serializers.ModelSerializer):
    # authors = AuthorSerializer()
    # author_id = serializers.Field(source='author.id')

    class Meta:
        model = Book
        exclude = ['slug']


class RecordSerializer(serializers.ModelSerializer):
    # publisher = PublisherSerializer()
    book = BookSerializer()
    publisher_id = serializers.Field(source='publisher.id')

    class Meta:
        model = Record
        exclude = ['slug', 'publisher']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction