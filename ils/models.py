import datetime
import os

import dbsettings
from django.core.urlresolvers import reverse
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from core.models import Language
from app.utils.forms import unique_slugify
from users.models import User
from app.utils.flexible_date import FlexibleDateField


BOOK_TYPES = (
    ('Reference', 'Reference'),
    ('Circulative', 'Circulative')
)


class MyCustomDate(models.Model):
    date = FlexibleDateField(max_length=250)

    def __unicode__(self):
        return unicode(self.date)


class Subject(MPTTModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=254, null=True, blank=True)
    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='children')
    slug = models.SlugField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super(Subject, self).save(*args, **kwargs)


class Author(models.Model):
    name = models.CharField(max_length=255)
    identifier = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super(Author, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('view_author', kwargs={'slug': self.slug})


class Place(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super(Place, self).save(*args, **kwargs)


class Publisher(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super(Publisher, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('view_publisher', kwargs={'slug': self.slug})


class Book(models.Model):
    title = models.CharField(max_length=254)
    subtitle = models.CharField(max_length=254, null=True, blank=True)
    subjects = models.ManyToManyField(Subject)
    slug = models.SlugField(max_length=255, blank=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        unique_slugify(self, self.title)
        super(Book, self).save(*args, **kwargs)


class Record(models.Model):
    edition = models.CharField(max_length=254, null=True, blank=True)
    formats = (
        ('Paperback', 'Paperback'),
        ('Hardcover', 'Hardcover'),
        ('eBook', 'eBook')
    )
    format = models.CharField(
        max_length=10,
        default='Paperback',
        choices=formats)
    pagination = models.CharField(max_length=254, null=True, blank=True)
    isbn13 = models.CharField(max_length=254, null=True, blank=True)
    authors = models.ManyToManyField(Author, blank=True)
    languages = models.ManyToManyField(Language, blank=True)
    # date_of_publication = FlexibleDateField(null=True, blank=True)
    date_of_publication = FlexibleDateField(null=True, blank=True)
    # publication_has_month = models.BooleanField(default=True)
    # publication_has_day = models.BooleanField(default=True)
    price = models.FloatField(null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True, default=1)
    types = (
        ('Reference', 'Reference'),
        ('Circulative', 'Circulative')
    )
    type = models.CharField(choices=types, max_length=11)
    book = models.ForeignKey(Book, blank=True)
    # openlibrary_url = models.URLField(blank=True, null=True)
    # thumbnail = models.ImageField(
    # blank=True, null=True, upload_to='ils/thumbnails/')
    small_cover = models.ImageField(
        blank=True,
        null=True,
        upload_to='ils/covers/small/')
    medium_cover = models.ImageField(
        blank=True,
        null=True,
        upload_to='ils/covers/medium/')
    large_cover = models.ImageField(
        blank=True,
        null=True,
        upload_to='ils/covers/large/')
    publisher = models.ForeignKey(Publisher, blank=True, null=True)
    date_added = models.DateField()
    goodreads_id = models.PositiveIntegerField(null=True, blank=True)
    librarything_id = models.PositiveIntegerField(null=True, blank=True)
    openlibrary_id = models.CharField(max_length=254, null=True, blank=True)
    lcc = models.CharField(max_length=100, null=True, blank=True)
    ddc = models.CharField(max_length=100, null=True, blank=True)
    lccn_id = models.CharField(max_length=100, null=True, blank=True)
    oclc_id = models.CharField(max_length=100, null=True, blank=True)
    published_places = models.ManyToManyField(Place, blank=True)
    weight = models.CharField(max_length=254, null=True, blank=True)
    dimensions = models.CharField(max_length=254, null=True, blank=True)
    by_statement = models.CharField(max_length=254, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    excerpt = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        title = self.book.title
        if self.edition:
            title = title + ' (' + self.edition + ')'
        if self.format != 'Paperback':
            title = title + ' [' + self.format + ']'
        return title

    def ebooks(self, book_format=None):
        ebooks = BookFile.objects.filter(record=self)
        if book_format:
            books = []
            for ebook in ebooks:
                if ebook.format == book_format:
                    books.append(ebook)
            return books
        else:
            return ebooks

    # def published_date(self):
    #     if not self.date_of_publication:
    #         return None
    #     if self.publication_has_day:
    #         return self.date_of_publication
    #     elif self.publication_has_month:
    #         return self.date_of_publication.strftime('%B %Y')
    #     elif self.date_of_publication:
    #         return self.date_of_publication

    def get_absolute_url(self):
        return reverse('view_record', kwargs={'pk': self.id})

    def in_circulation(self):
        return Transaction.objects.filter(record=self, return_date=None)

    def get_small_cover(self):
        return self.small_cover or self.medium_cover or self.large_cover

    def get_medium_cover(self):
        return self.medium_cover or self.small_cover or self.large_cover

    def get_large_cover(self):
        return self.large_cover or self.medium_cover or self.small_cover


class BookFile(models.Model):
    file = models.FileField(upload_to='ils/books/')
    record = models.ForeignKey(Record, related_name='files')

    def format(self):
        try:
            filename = self.file.file.name
            ext = os.path.splitext(filename)[1]
            if ext[0] == '.':
                ext = ext[1:]
            if ext == 'txt':
                return 'text'
            return ext
        except:
            return 'File does not exist'

    format = property(format)

    def __unicode__(self):
        return unicode(self.record) + ' {' + self.format + '}'


class Transaction(models.Model):
    record = models.ForeignKey(Record)
    user = models.ForeignKey(User, related_name='transactions')
    borrow_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    returned = models.BooleanField(default=False)
    fine_per_day = models.FloatField()
    fine_paid = models.FloatField(default=False)

    @staticmethod
    def new():
        transaction = Transaction()
        transaction.borrow_date = datetime.datetime.today().date()
        from ils.models import library_setting as setting

        transaction.due_date = transaction.borrow_date + \
                               datetime.timedelta(days=setting.borrow_days)
        transaction.fine_per_day = setting.fine_per_day
        return transaction

    def __unicode__(self):
        return unicode(self.record) + ' | ' + unicode(self.user)


class LibrarySetting(dbsettings.Group):
    fine_per_day = dbsettings.FloatValue(default=2)
    borrow_days = dbsettings.PositiveIntegerValue(default=7)
    default_type = dbsettings.StringValue(
        choices=BOOK_TYPES,
        default='Circulative')


library_setting = LibrarySetting('Library Settings')


def not_returned(self):
    transactions = Transaction.objects.filter(user=self, return_date=None)
    return transactions


def past_due(self):
    transactions = Transaction.objects.filter(
        user=self,
        return_date=None,
        due_date__lt=datetime.datetime.today())
    return transactions


User.add_to_class('not_returned', not_returned)
User.add_to_class('past_due', past_due)