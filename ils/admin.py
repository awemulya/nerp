from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import Book, Record, Author, Subject, Transaction, BookFile, \
    Publisher, LibrarySetting

admin.site.register(Book)
admin.site.register(BookFile)
admin.site.register(Record)
admin.site.register(Subject)
admin.site.register(Author)
admin.site.register(Transaction)
admin.site.register(Publisher)
admin.site.register(LibrarySetting, SingletonModelAdmin)
