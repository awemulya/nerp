from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from app.utils.helpers import title_case
from core.models import Language
from ils.forms import RecordFormRelatedFields, RecordFormUnrelatedFields,\
     BookForm, SubjectForm, AuthorForm, PlaceForm,\
     PublisherForm, LanguageForm, OutgoingForm, IncomingForm, PatronForm
from ils.models import library_setting as setting

from ils.serializers import RecordSerializer, AuthorSerializer,\
     PublisherSerializer, PlaceSerializer, SubjectSerializer, BookSerializer, \
     TransactionSerializer
from core.serializers import LanguageSerializer
from . import isbn as isbnpy
import urllib2
import urllib
import json
from django.http import HttpResponse
from rest_framework import generics

from .models import Record, Author, Publisher, Book, Subject,\
    Place, BookFile, Transaction

import os
from django.core.files import File
from datetime import datetime
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from users.models import User, group_required
# from haystack.query import SearchQuerySet
from ils.forms import LibrarySearchForm
import pdb


@group_required('Librarian')
def authors_as_json(request):
    items = Author.objects.all()
    items_data = AuthorSerializer(items, many=True).data
    return JsonResponse(items_data, safe=False)


@group_required('Librarian')
def publishers_as_json(request):
    items = Publisher.objects.all()
    items_data = PublisherSerializer(items, many=True).data
    return JsonResponse(items_data, safe=False)


@group_required('Librarian')
def subjects_as_json(request):
    items = Subject.objects.all()
    items_data = SubjectSerializer(items, many=True).data
    return JsonResponse(items_data, safe=False)


@group_required('Librarian')
def books_as_json(request):
    items = Book.objects.all()
    items_data = BookSerializer(items, many=True).data
    return JsonResponse(items_data, safe=False)


@group_required('Librarian')  # noqa
def acquisition(request):
    record_data = {}
    record = None
    if request.GET.get('isbn'):
        isbn = request.GET.get('isbn')
        if isbnpy.isValid(isbn):
            if isbnpy.isI10(isbn):
                isbn = isbnpy.convert(isbn)
            url = 'http://openlibrary.org/api/volumes/brief/json/isbn:' + isbn
            response = urllib2.urlopen(url)
            # response = urllib2.urlopen('http://127.0.0.1/json/3.json')
            data = json.load(response)
            if data == {}:
                print 123
                record_data['isbn13'] = isbn
                record_form = RecordForm(instance=record)
                return render(
                    request, 'acquisition.html', {
                        'data': record_data, 'form': record_form})
            data = data.itervalues().next()['records'].itervalues().next()

            try:
                record = Record.objects.get(isbn13=isbn)
                new_record = False
            except Record.DoesNotExist:
                record = Record(isbn13=isbn)
                new_record = True
                # pp(data)
            if record.book_id:
                book = record.book
            else:
                book = Book()
 
            book.title = data['data']['title']
            if 'subtitle' in data['details']['details']:
                book.subtitle = data['details']['details']['subtitle']
            book.save()

            if 'pagination' in data['details']['details']:
                record.pagination = data['data']['pagination']
            elif 'number_of_pages' in data['details']['details']:
                record.pagination = str(
                    data['data']['number_of_pages']) + ' p.'

            if 'physical_format' in data['details']['details']:
                record.format = data['details']['details']['physical_format']
                if record.format.startswith('electronic'):
                    record.format = 'eBook'
                    # record.openlibrary_url = data['data']['url']

            if 'weight' in data['details']['details']:
                record.weight = data['details']['details'].get('weight')
            if 'physical_dimensions' in data['details']['details']:
                record.dimensions = data['details'][
                    'details'].get('physical_dimensions')

            if 'classifications' in data['data']:
                if 'dewey_decimal_class' in data['data']['classifications']:
                    record.ddc = data['data']['classifications'].get(
                        'dewey_decimal_class')[0]
                if 'lc_classifications' in data['data']['classifications']:
                    record.lcc = data['data']['classifications'].get(
                        'lc_classifications')[0]

            try:
                record.date_of_publication = datetime.strptime(
                    data['data']['publish_date'],
                    '%B %d, %Y').date()
                record.publication_has_month = True
                record.publication_has_day = True
            except ValueError:
                try:
                    record.date_of_publication = datetime.strptime(
                        data['data']['publish_date'],
                        '%Y').date()
                    record.publication_has_month = False
                    record.publication_has_day = False
                except ValueError:
                    try:
                        record.date_of_publication = datetime.strptime(
                            data['data']['publish_date'],
                            '%B %Y').date()
                        record.publication_has_day = False
                        record.publication_has_month = True
                    except ValueError:
                        record.date_of_publication = datetime.strptime(
                            data['data']['publish_date'],
                            '%m/%d/%Y').date()
                        record.publication_has_day = True
                        record.publication_has_month = True

            if 'identifiers' in data['data']:
                if 'openlibrary' in data['data']['identifiers']:
                    record.openlibrary_id = data['data'][
                        'identifiers']['openlibrary'][0]
                if 'goodreads' in data['data']['identifiers']:
                    record.goodreads_id = data['data'][
                        'identifiers']['goodreads'][0]
                if 'librarything' in data['data']['identifiers']:
                    record.librarything_id = data['data'][
                        'identifiers']['librarything'][0]
                if 'oclc' in data['data']['identifiers']:
                    record.oclc_id = data['data']['identifiers']['oclc'][0]
                if 'lccn' in data['data']['identifiers']:
                    record.lccn_id = data['data']['identifiers']['lccn'][0]

            if 'by_statement' in data['data']:
                record.by_statement = data['data'].get('by_statement')

            if 'notes' in data['data']:
                record.notes = data['data'].get('notes')

            if 'excerpts' in data['data']:
                record.excerpt = data['data'].get('excerpts')[0].get('text')

            record.book = book

            record.type = setting.default_type

            if new_record:
                record.date_added = datetime.today()
            record.save()

            if 'languages' in data['details']['details']:
                record.languages.clear()
                for lang in data['details']['details']['languages']:
                    lang_key = lang['key'].replace('/languages/', '')
                    try:
                        book_lang = Language.objects.get(code=lang_key)
                    except Language.DoesNotExist:
                        try:
                            book_lang = Language.objects.get(code=lang_key[:-1])
                        except Language.DoesNotExist:
                            raise Exception(
                                "Please add a language with code " +
                                lang_key +
                                " or " +
                                lang_key[
                                :-
                                1] +
                                " first!")
                    record.languages.add(book_lang)

            if 'publish_places' in data['data']:
                record.published_places.clear()
                for place in data['data']['publish_places']:
                    try:
                        published_place = Place.objects.get(name=place['name'])
                    except Place.DoesNotExist:
                        published_place = Place(name=place['name'])
                    published_place.save()
                    record.published_places.add(published_place)

            record.authors.clear()
            if 'authors' in data['details']['details']:
                for author in data['details']['details']['authors']:
                    author_key = author['key'].replace('/authors/', '')
                    try:
                        book_author = Author.objects.get(identifier=author_key)
                    except Author.DoesNotExist:
                        book_author = Author(identifier=author_key)
                    book_author.name = author['name']
                    book_author.save()
                    record.authors.add(book_author)
            elif 'authors' in data['data']:
                for author in data['data']['authors']:
                    author_key = author['url'].replace(
                        'http://openlibrary.org/authors/',
                        '')
                    try:
                        book_author = Author.objects.get(identifier=author_key)
                    except Author.DoesNotExist:
                        book_author = Author(identifier=author_key)
                    book_author.name = author['name']
                    book_author.save()
                    record.authors.add(book_author)

            if 'ebooks' in data['data']:
                if 'formats' in data['data']['ebooks'][0]:
                    formats = data['data']['ebooks'][0]['formats']
                    for book_format in formats:
                        ebooks = record.ebooks(book_format)
                        for ebook in ebooks:
                            ebook.delete()
                        if 'url' in formats[book_format]:
                            url = formats[book_format].get('url')
                            result = urllib.urlretrieve(url)
                            book_file = BookFile(record=record)
                            book_file.file.save(
                                os.path.basename(url),
                                File(open(result[0]))
                            )
                            book_file.save()

            subjects = None
            if 'subjects' in data['details']['details']:
                subjects = data['details']['details']['subjects']
            elif 'subjects' in data['data']:
                subjects = data['data']['subjects']
            if subjects:
                record.book.subjects.clear()
                for subject in subjects:
                    if isinstance(subject, dict):
                        subject = title_case(subject['name'])
                    try:
                        book_subject = Subject.objects.get(name=subject)
                    except Subject.DoesNotExist:
                        book_subject = Subject(name=subject)
                    book_subject.save()
                    record.book.subjects.add(book_subject)

            # record.publishers.clear()
            # for publisher in data['details']['details']['publishers']:
            # try:
            # book_publisher = Publisher.objects.get(name=publisher['name'])
            # except Publisher.DoesNotExist:
            # book_publisher = Publisher(name=publisher['name'])
            # book_publisher.save()
            # record.publishers.add(book_publisher)
            try:
                book_publisher = Publisher.objects.get(
                    name=data['details']['details']['publishers'][0])
            except Publisher.DoesNotExist:
                book_publisher = Publisher(
                    name=data['details']['details']['publishers'][0])
                book_publisher.save()
            record.publisher = book_publisher

            if 'cover' in data['data']:

                if 'large' in data['data']['cover']:
                    cover_url = data['data']['cover']['large']
                    result = urllib.urlretrieve(cover_url)
                    record.large_cover.save(
                        os.path.basename(cover_url),
                        File(open(result[0]))
                    )
                if 'medium' in data['data']['cover']:
                    cover_url = data['data']['cover']['medium']
                    result = urllib.urlretrieve(cover_url)
                    record.medium_cover.save(
                        os.path.basename(cover_url),
                        File(open(result[0]))
                    )

                if 'small' in data['data']['cover']:
                    cover_url = data['data']['cover']['small']
                    result = urllib.urlretrieve(cover_url)
                    record.small_cover.save(
                        os.path.basename(cover_url),
                        File(open(result[0]))
                    )

                    # thumbnail_url = data['details']['thumbnail_url']
                    # result = urllib.urlretrieve(thumbnail_url)
                    # record.thumbnail.save(
                    # os.path.basename(thumbnail_url),

                record_data = RecordSerializer(record).data

    record_form = RecordForm(instance=record)

    return render(
        request, 'acquisition.html', {
            'data': record_data, 'form': record_form})


@group_required('Librarian')  # noqa
def save_acquisition(request):
    if request.POST.get('book').isnumeric():
        book = Book.objects.get(id=request.POST.get('book'))
        new_book = False
    else:
        book = Book(title=request.POST.get('book'))
        new_book = True
    book.subtitle = request.POST.get('subtitle')
    book.save()

    if request.POST.get('isbn'):
        isbn = request.POST.get('isbn')
        if isbnpy.isValid(isbn):
            if isbnpy.isI10(isbn):
                isbn = isbnpy.convert(isbn)
            try:
                record = Record.objects.get(isbn13=isbn)
                new_record = False
            except Record.DoesNotExist:
                record = Record(isbn13=isbn)
                new_record = True
    else:
        if not new_book:
            try:
                record = Record.objects.get(
                    book=book,
                    edition=request.POST.get('book'))
                new_record = False
            except Record.DoesNotExist:
                record = Record(book=book)
                new_record = True
        else:
            record = Record(book=book)
            new_record = True

    record.book = book
    record.format = request.POST.get('format')
    if record.format != 'ebook':
        if new_record:
            record.quantity = request.POST.get('quantity')
        else:
            record.quantity += int(request.POST.get('quantity'))

    record.excerpt = request.POST.get('excerpt')
    record.edition = request.POST.get('edition')
    record.notes = request.POST.get('notes')
    record.ddc = request.POST.get('ddc')
    record.lcc = request.POST.get('lcc')
    record.pagination = request.POST.get('pagination')
    record.format = request.POST.get('format')
    record.type = request.POST.get('type')
    if record.format != 'eBook':
        record.quantity = request.POST.get('quantity')

    record.publication_has_month = False
    record.publication_has_day = False
    if request.POST.get('year'):
        dt = datetime(int(request.POST.get('year')), 1, 1)
        if request.POST.get('month'):
            record.publication_has_month = True
            dt = dt.replace(month=int(request.POST.get('month')))
            if request.POST.get('day'):
                record.publication_has_day = True
                dt = dt.replace(day=int(request.POST.get('day')))
        record.date_of_publication = dt
    else:
        record.date_of_publication = None

    if request.FILES.get('small_cover'):
        record.small_cover = request.FILES.get('small_cover')
    if request.FILES.get('medium_cover'):
        record.medium_cover = request.FILES.get('medium_cover')
    if request.FILES.get('large_cover'):
        record.large_cover = request.FILES.get('large_cover')

    if not record.date_added:
        record.date_added = datetime.today()

    record.save()

    if request.FILES.get('ebook'):
        ebooks = request.FILES.getlist('ebook')
        for ebook in ebooks:
            ebook_file = BookFile(record=record, file=ebook)
            existing_files = record.ebooks(ebook_file.format)
            for existing_file in existing_files:
                existing_file.delete()
            ebook_file.save()

    book.subjects.clear()
    for subject in request.POST.getlist('subjects'):
        if subject.isnumeric():
            book.subjects.add(Subject.objects.get(id=subject))
        else:
            new_subject = Subject(name=subject)
            new_subject.save()
            book.subjects.add(new_subject)

    record.authors.clear()
    for author in request.POST.getlist('authors'):
        if author.isnumeric():
            record.authors.add(Author.objects.get(id=author))
        else:
            new_author = Author(name=author)
            new_author.save()
            record.authors.add(new_author)

    record.languages.clear()
    for language in request.POST.getlist('languages'):
        record.languages.add(Language.objects.get(id=language))

    publisher = request.POST.get('publisher')
    if publisher:
        if publisher.isnumeric():
            record.publisher_id = publisher
        else:
            new_publisher = Publisher(name=publisher)
            new_publisher.save()
            record.publisher = new_publisher

    record.save()

    return redirect(reverse_lazy('view_record', kwargs={'pk': record.id}))


@group_required('Librarian')
def outgoing(request, pk=None):
    transaction = Transaction.new()
    if pk:
        transaction.record = Record.objects.get(id=pk)
    form = OutgoingForm(instance=transaction)
    return render(request, 'outgoing.html', {'form': form})


@group_required('Librarian')
def save_outgoing(request):
    error = False
    transaction = Transaction.new()
    transaction.user_id = request.POST.get('user')
    transaction.borrow_date = request.POST.get('borrow_date')
    transaction.due_date = request.POST.get('due_date')
    transaction.record_id = request.POST.get('record')
    if request.POST.get('isbn'):
        isbn = request.POST.get('isbn')
        if isbnpy.isValid(isbn):
            if isbnpy.isI10(isbn):
                isbn = isbnpy.convert(isbn)
            try:
                transaction.record = Record.objects.get(isbn13=isbn)
            except Record.DoesNotExist:
                error = 'No books with provided ISBN in library database.'
        else:
            error = 'Invalid ISBN!'
        if error:
            raise Exception(error)
    transaction.save()
    messages.success(request, 'Checked Out!')
    return redirect(
        reverse_lazy(
            'view_record',
            kwargs={
                'pk': transaction.record_id}))


@group_required('Librarian')
def incoming(request, transaction_pk):
    transaction = Transaction.objects.get(id=transaction_pk)
    if request.POST:

        form = IncomingForm(data=request.POST, instance=transaction)
        transaction = form.save()
        if not request.POST.get('return_date'):
            transaction.return_date = datetime.today()
        transaction.save()
        messages.success(request, 'Book Returned!')
        return redirect(
            reverse_lazy(
                'view_record',
                kwargs={
                    'pk': transaction.record_id}))

    form = IncomingForm(instance=transaction)
    data = TransactionSerializer(transaction).data
    return render(request, 'incoming.html', {'form': form, 'data': data})


def view_record(request, pk=None):
    record = get_object_or_404(Record, pk=pk)
    transactions = Transaction.objects.filter(record=record)
    return render(
        request, 'view_record.html', {
            'record': record, 'transactions': transactions})


@group_required('Librarian')
def list_patrons(request):
    patrons = User.objects.by_group('Patron')
    return render(request, 'list_patrons.html', {'patrons': patrons})


# TODO allow self
@group_required('Librarian')
def view_patron(request, pk):
    patron = get_object_or_404(User, pk=pk)
    transactions = Transaction.objects.filter(user=patron)
    return render(
        request, 'view_patron.html', {
            'patron': patron, 'transactions': transactions})


@group_required('Librarian')
def list_transactions(request):
    transactions = Transaction.objects.all()
    return render(
        request, 'list_transactions.html', {
            'transactions': transactions})


def list_records(request):
    records = Record.objects.all()
    return render(request, 'list_records.html', {'records': records})


def list_authors(request):
    authors = Author.objects.all()
    return render(request, 'list_authors.html', {'authors': authors})


def view_author(request, slug):
    author = Author.objects.get(slug=slug)
    return render(request, 'view_author.html', {'author': author})


def view_publisher(request, slug):
    publisher = Publisher.objects.get(slug=slug)
    return render(request, 'view_publisher.html', {'publisher': publisher})


def list_publishers(request):
    objects = Publisher.objects.all()
    return render(request, 'list_publishers.html', {'objects': objects})


def index(request):
    form = LibrarySearchForm()
    return render(request, 'library_index.html', {'form': form})


def isbn_to_record(request):
    isbn = request.POST.get('isbn')
    if isbn and isbnpy.isValid(isbn):
        if isbnpy.isI10(isbn):
            isbn = isbnpy.convert(isbn)
        try:
            record = Record.objects.get(isbn13=isbn)
        except Record.DoesNotExist:
            messages.error(request, 'Book not added yet, add it first!')
            return redirect(reverse_lazy('acquisition') + '?isbn=' + isbn)
        return redirect(reverse_lazy('view_record', kwargs={'pk': record.id}))
    else:
        messages.error(request, 'Invalid ISBN!')
        return redirect(reverse_lazy('library_index'))


def list_ebooks(request):
    records = Record.objects.filter(files__isnull=False).distinct()
    return render(request, 'list_records.html', {'records': records})


@group_required('Librarian')
def patron_form(request, pk=None):
    if pk:
        item = get_object_or_404(User, id=pk)
        scenario = 'Edit'
    else:
        item = User()
        scenario = 'Add'
    if request.POST:
        form = PatronForm(data=request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            item.set_password(form.cleaned_data['password'])
            item.save()
            if not item.add_to_group('Patron'):
                raise Exception('Add group Patron first!')
                # if request.is_ajax():
            # return render(request, 'callback.html', {'obj':
            # ItemSerializer(item).data})
            return redirect('list_patrons')
    else:
        form = PatronForm(instance=item)
        # if request.is_ajax():
    # base_template = 'modal.html'
    # else:
    # base_template = 'base.html'
    return render(request, 'patron_form.html', {
        'scenario': scenario,
        'form': form,
        # 'base_template': base_template,
    })


def search(request, keyword=None):
    # if keyword:
    # results = SearchQuerySet().filter(content=keyword)
    if request.GET:
        form = LibrarySearchForm(data=request.GET)

    else:
        form = LibrarySearchForm()
    return render(request, 'library_search.html', {'form': form})


class PlaceList(generics.ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class SubjectList(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class PublisherList(generics.ListCreateAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class LanguageList(generics.ListCreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class RecordView(View):
    record_form_related_fields = RecordFormRelatedFields
    record_form_unrelated_fields = RecordFormUnrelatedFields
    book_form = BookForm
    author_form = AuthorForm
    place_form = PlaceForm
    publisher_form = PublisherForm
    lan_form = LanguageForm
    subject_form = SubjectForm

    rr_initial = {'key': 'value'}
    ru_initial = {'key': 'value'}
    b_initial = {'key': 'value'}
    a_initial = {'key': 'value'}
    p_initial = {'key': 'value'}
    pub_initial = {'key': 'value'}
    l_initial = {'key': 'value'}
    sub_initial = {'key': 'value'}

    template_name = 'acquisition1.html'

    def get_objects(self, cls, *dl, **kwargs):
        # pdb.set_trace()
        if kwargs:
            return cls.objects.filter(**kwargs)
        if dl:
            objs = []
            for dic in dl:
                objs.append(cls.objects.get_or_create(**dic))
            # pdb.set_trace()
            return objs

    def get_from_api(self, **kwargs):
        data = kwargs['data']
        lookup_fields = kwargs['lookup_fields']
        lookup_path = kwargs['lookup_path']
        if 'form_fields' in kwargs:
            form_fields = kwargs['form_fields']
        if 'multiselect' in kwargs:
            multiselect = kwargs['multiselect']
        else:
            multiselect = False
        value = []
        vl = []
        # dictionary to filter
        dictionary = {}
        lod = []

        for lp in lookup_path:
            data = data[lp]

        if 'cls' in kwargs:
            cls = kwargs['cls']

            if multiselect:

                for field in lookup_fields:
                    if type(data[field]) is list and type(data[field][0]) is unicode:

                        for item in data[field]:
                            lol = [item]
                            vl.append(lol)
                        for val in vl:
                            for f_field, v in zip(form_fields, val):
                                dictionary[f_field] = v
                            lod.append(dictionary)
                        objs = self.get_objects(cls, *lod)
                        if objs:
                            ll = []
                            for o in objs:
                                ll.append(o[0].id)
                            return ll
                    elif type(data[field]) is unicode:
                        dictn = {}
                        val = data[field]
                        dictn[form_fields[0]] = val
                        objs = self.get_objects(cls, **dictn)
                        if objs:
                            ll = []
                            for o in objs:
                                ll.append(o.id)
                            return ll
                        

            else:
                for field in lookup_fields:
                    if field in data:
                        value.append(data[field])
                    else:
                        value.append(None)

                for f_field, v in zip(form_fields, value):
                    if v is not None:
                        dictionary[f_field] = v
                objs = self.get_objects(cls, **dictionary)
                if objs:
                    ll = []
                    for o in objs:
                        ll.append(o.id)
                # pdb.set_trace()
                # if select then return number of mselect then return list
                    return ll[0]
                else:
                    instance = kwargs['form_ins']
                    for f_field, va in zip(form_fields, value):
                        instance[f_field] = va
        else:
            for field in lookup_fields:
                value.append(data[field])
            instance = kwargs['form_ins']
            for f_field, va in zip(form_fields, value):
                instance[f_field] = va
         
        pass

    def populate(self, isbn):
        response = urllib2.urlopen('https://www.googleapis.com' +
                                   '/books/v1/volumes?q=search+isbn9780439023481')
        data = json.load(response)
        self.rr_initial = {'book': self.get_from_api(
                           data=data['items'][0],
                           lookup_path=['volumeInfo'],
                           lookup_fields=['title', 'subtitle'],
                           # Specify only if this field is related
                           cls=Book,
                           multiselect=False,
                           # In case we need to populate the field
                           form_ins=self.b_initial,
                           form_fields=['title', 'subtitle']
                           ),

                           'published_place': [],

                           'authors': self.get_from_api(
                            data=data['items'][0],
                            lookup_path=['volumeInfo'],
                            lookup_fields=['authors'],
                            cls=Author,
                            multiselect=True,
                            form_fields=['name'],
                            ),

                           'publisher': self.get_from_api(
                            data=data['items'][0],
                            lookup_path=['volumeInfo'],
                            lookup_fields=['publisher'],
                            cls=Publisher,
                            form_ins=self.pub_initial,
                            form_fields=['name']
                            ),

                           'languages': self.get_from_api(
                            data=data['items'][0],
                            lookup_path=['volumeInfo'],
                            lookup_fields=['language'],
                            cls=Language,
                            multiselect=True,
                            form_fields=['code'],

                            ),

                           }
        return HttpResponse('hahahah')

    def get(self, request, *args, **kwargs):
        if request.GET.get('isbn13'):
            isbn = request.GET['isbn13']
            if isbnpy.isValid(isbn):
                if isbnpy.isI10(isbn):
                    isbn = isbnpy.convert(isbn)
                    self.populate(isbn)
        rr_form = self.record_form_related_fields(initial=self.rr_initial)
        ru_form = self.record_form_unrelated_fields(initial=self.ru_initial)
        b_form = self.book_form(initial=self.b_initial)
        a_form = self.author_form(initial=self.a_initial)
        p_form = self.place_form(initial=self.p_initial)
        pub_form = self.publisher_form(initial=self.pub_initial)
        l_form = self.lan_form(initial=self.l_initial)
        sub_form = self.subject_form(initial=self.sub_initial)
        return render(request, self.template_name, {'rr_form': rr_form,
                                                    'ru_form': ru_form,
                                                    'b_form': b_form,
                                                    'a_form': a_form,
                                                    'p_form': p_form,
                                                    'pub_form': pub_form,
                                                    'l_form': l_form,
                                                    'sub_form': sub_form,
                                                    })

    def post(self, request, *args, **kwargs):
        pass

        # def get_from_api_select(self, **kwargs):
        # data = kwargs['data']
        # lookup_fields = kwargs['lookup_fields']
        # lookup_path = kwargs['lookup_path']
        # form_fields = kwargs['form_fields']
        # value = []
        # # dictionary to filter
        # dictionary = {}

        # for lp in lookup_path:
        #     data = data[lp]

        # for i, field in enumerate(lookup_fields):
        #     value.append(data[field])

        # if kwargs['cls']:
        #     cls = kwargs['cls']
        #     for f_field, v in zip(form_fields, value):
        #         dictionary[f_field] = v
        #     objs = cls.objects.filter(**dictionary)
        #     if objs:
        #         ll = []
        #         for o in objs:
        #             ll.append(o.id)
        #         # pdb.set_trace()
        #         # if select then return number of mselect then return list
        #         return ll[0]
        #     else:
        #         instance = kwargs['form_ins']
        #         for f_field, va in zip(form_fields, value):
        #             instance[f_field] = va
        # pass
