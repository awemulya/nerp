from django import forms
from django.utils.translation import ugettext_lazy as _
from haystack.forms import ModelSearchForm

from app.utils.forms import KOModelForm
from ils.models import Record, Transaction, Book, Author, Place, Publisher, Subject
from core.models import Language
from users.models import User


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = '__all__'


class RecordForm(KOModelForm):
    class Meta:
        model = Record
        fields = '__all__'
        widgets = {
            'notes': forms.Textarea(attrs={'cols': 0, 'rows': 0}),
            'excerpt': forms.Textarea(attrs={'cols': 0, 'rows': 0}),
            'description': forms.Textarea(attrs={'cols': 0, 'rows': 0})
        }


class BookForm(KOModelForm):
    class Meta:
        model = Book
        exclude = ['slug']
        # labels = {
        #     'title': _('Book Title'),
        #     'subtitle': _('Book Subtitle'),
        #     'subjects': _('Book Subjects')
        # }
        help_texts = {
            'subjects': ('')
        }
        widgets = {
            'title': forms.TextInput(attrs={'required': 'true'}),
            'subjects': forms.SelectMultiple(attrs={'required': 'true'}),
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ['slug', 'identifier']


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        exclude = ['slug']


class PublisherForm(KOModelForm):
    class Meta:
        model = Publisher
        exclude = ['slug']
        labels = {
            'name': _('Publisher')
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        exclude = ['slug']


class OutgoingForm(forms.ModelForm):
    borrow_date = forms.CharField(widget=forms.TextInput(attrs={'data-date-format': 'yyyy-mm-dd', 'class': 'form-control'}),
                                  required=False)
    due_date = forms.CharField(widget=forms.TextInput(attrs={'data-date-format': 'yyyy-mm-dd', 'class': 'form-control'}),
                               required=False)
    isbn = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='ISBN')

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


class PatronForm(KOModelForm):
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

        for (name, field) in self.fields.items():
            widget = field.widget
            exclude_form_control = ['CheckboxInput', 'RadioSelect', 'CheckboxSelectMultiple']
            if widget.__class__.__name__ in exclude_form_control:
                continue
            if 'class' in widget.attrs:
                widget.attrs['class'] += 'form-control'
            else:
                widget.attrs['class'] = 'form-control'
