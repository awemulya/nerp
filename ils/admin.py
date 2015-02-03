from django.contrib import admin
from .models import Book, Record, Author, Subject, Transaction, BookFile, \
    Publisher
from .models import MyCustomDate

admin.site.register(Book)
admin.site.register(BookFile)
admin.site.register(Record)
admin.site.register(Subject)
admin.site.register(Author)
admin.site.register(Transaction)
admin.site.register(Publisher)
admin.site.register(MyCustomDate)
