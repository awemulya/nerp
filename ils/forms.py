from django import forms
from app.utils.forms import KOModelForm
from models import Record, Transaction, Book, Author, Place, Publisher, Subject
from core.models import Language
from users.models import User
from django.utils.translation import ugettext_lazy as _
from haystack.forms import SearchForm, ModelSearchForm


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language


class RecordFormRelatedFields(forms.ModelForm):
    class Meta:
        model = Record
        include = ['book',
                   'published_places',
                   'authors',
                   'publisher',
                   'languages',
                   ]
        widgets = {
            'book': forms.SelectMultiple(attrs={'cols': 80, 'rows': 20}),
        }


class RecordFormUnrelatedFields(forms.ModelForm):
    class Meta:
        model = Record
        exclude = ['book',
                   'published_places',
                   'authors',
                   'publisher',
                   'languages',
                   ]


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['slug']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ['slug', 'identifier']


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        exclude = ['slug']


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        exclude = ['slug']


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        exclude = ['slug']


class OutgoingForm(forms.ModelForm):
    isbn = forms.CharField(label='ISBN')

    def __init__(self, *args, **kwargs):
        super(OutgoingForm, self).__init__(*args, **kwargs)
        self.fields['user'].label = 'Patron'
        self.fields['record'].empty_label = None
        self.fields['user'].empty_label = None
        self.fields['user'].queryset = User.objects.by_group('Patron')

    class Meta:
        model = Transaction
        exclude = ['fine_paid', 'fine_per_day', 'returned', 'return_date']


class IncomingForm(KOModelForm):
    def __init__(self, *args, **kwargs):
        super(IncomingForm, self).__init__(*args, **kwargs)
        self.fields['user'].label = 'Patron'
        self.fields['record'].empty_label = None
        self.fields['user'].empty_label = None
        self.fields['user'].queryset = User.objects.by_group('Patron')

    class Meta:
        model = Transaction
        exclude = ()


class PatronForm(forms.ModelForm):
    password1 = forms.CharField(max_length=128, widget=forms.PasswordInput, label=_("Password (again)"))

    class Meta:
        model = User
        exclude = ['last_login', 'is_active', 'is_staff', 'is_superuser', 'groups']


    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        else:
            return self.cleaned_data['username']

    def clean_email(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        existing = User.objects.filter(email__iexact=self.cleaned_data['email'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that email already exists."))
        else:
            return self.cleaned_data['email']


    def clean(self):
        """
        Verify that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password' in self.cleaned_data and 'password1' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data


class LibrarySearchForm(ModelSearchForm):
    # start_date = forms.DateField(required=False)
    # end_date = forms.DateField(required=False)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(LibrarySearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        # Check to see if a start_date was chosen.
        # if self.cleaned_data['start_date']:
        #     sqs = sqs.filter(pub_date__gte=self.cleaned_data['start_date'])
        #
        # # Check to see if an end_date was chosen.
        # if self.cleaned_data['end_date']:
        #     sqs = sqs.filter(pub_date__lte=self.cleaned_data['end_date'])

        return sqs

    def __init__(self, *args, **kwargs):
        super(LibrarySearchForm, self).__init__(*args, **kwargs)
        aa, bb = self.fields['models'].choices[2]
        self.fields['models'].choices[2] = (aa, 'Books')
        self.fields['models'].initial = ['ils.record']
