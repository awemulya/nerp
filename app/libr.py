# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils import translation

import os
import re

from django import forms
from django.forms import ModelChoiceField
from django.shortcuts import render, get_object_or_404, redirect
from modeltranslation.translator import TranslationOptions
from django.template.defaultfilters import slugify


def _slug_strip(value, separator='-'):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
        # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
        # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value


def unique_slugify(instance, value, slug_field_name='slug', queryset=None,
                   slug_separator='-'):
    """
    Calculates and stores a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len - len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


class ExtFileField(forms.FileField):
    """
    Same as forms.FileField, but you can specify a file extension whitelist.

    Traceback (most recent call last):
    ...
    ValidationError: [u'Not allowed filetype!']
    """

    def __init__(self, *args, **kwargs):
        ext_whitelist = kwargs.pop("ext_whitelist")
        self.ext_whitelist = [i.lower() for i in ext_whitelist]

        super(ExtFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ExtFileField, self).clean(*args, **kwargs)
        if data is None:
            if self.required:
                raise forms.ValidationError("This file is required")
            else:
                return
        elif data is not False:
            filename = data.name
            ext = os.path.splitext(filename)[1]
            ext = ext.lower()
            if ext not in self.ext_whitelist:
                file_types = ", ".join([i for i in self.ext_whitelist])
                error = "Only allowed file types are: %s" % file_types
                raise forms.ValidationError(error)


class KOModelForm(forms.ModelForm):
    class EmailTypeInput(forms.widgets.TextInput):
        input_type = 'email'

    class NumberTypeInput(forms.widgets.TextInput):
        input_type = 'number'

    class TelephoneTypeInput(forms.widgets.TextInput):
        input_type = 'tel'

    class DateTypeInput(forms.widgets.DateInput):
        input_type = 'date'

    class DateTimeTypeInput(forms.widgets.DateTimeInput):
        input_type = 'datetime'

    class TimeTypeInput(forms.widgets.TimeInput):
        input_type = 'time'

    def __init__(self, *args, **kwargs):
        super(KOModelForm, self).__init__(*args, **kwargs)
        self.refine()

    def refine(self):
        for (name, field) in self.fields.items():
            # add HTML5 required attribute for required fields
            if field.required:
                field.widget.attrs['required'] = 'required'
            field.widget.attrs['data-bind'] = 'value: ' + name


def invalid(row, required_fields):
    invalid_attrs = []
    for attr in required_fields:
        # if one of the required attributes isn't received or is an empty string
        if not attr in row or row.get(attr) == "":
            invalid_attrs.append(attr)
    if len(invalid_attrs) is 0:
        return False
    return invalid_attrs


def empty_to_none(o):
    if o == '':
        return None
    return o


def all_empty(row, required_fields):
    empty = True
    for attr in required_fields:
        # if one of the required attributes isn received or is not an empty string
        if attr in row and row.get(attr) != "":
            empty = False
    return empty


def save_model(model, values):
    for key, value in values.items():
        setattr(model, key, value)
    model.save()
    return model


def zero_for_none(obj):
    if obj is None:
        return 0
    else:
        return obj


def none_for_zero(obj):
    if not obj:
        return None
    else:
        return obj


def add(*args):
    total = 0
    for arg in args:
        if arg == '':
            arg = 0
        total += float(arg)
    return total


def ne2en(num, reverse=False):
    if num is None:
        return None
    dct = {
        '०': '0',
        '१': '1',
        '२': '2',
        '३': '3',
        '४': '4',
        '५': '5',
        '६': '6',
        '७': '7',
        '८': '8',
        '९': '9'
    }
    if reverse:
        dct = dict((v, k) for k, v in dct.iteritems())
    pattern = re.compile('|'.join(dct.keys()))
    grouper = lambda x: dct[x.group()]
    num = unicode(num).encode()
    result = pattern.sub(grouper, num)
    return result

    # devanagari_nums = ('०','१','२','३','४','५','६','७','८','९')
    # return ''.join(devanagari_nums[int(digit)] for digit in str(n))


def en2ne(n):
    return ne2en(n, reverse=True)


def transl(s):
    lang = translation.get_language()
    lang = lang.split('-')[0]
    if lang == 'en':
        return ne2en(s)
    elif lang == 'ne':
        return en2ne(s)


class UserModelChoiceField(ModelChoiceField):
    '''
    A ModelChoiceField to represent User
    select boxes in the Auto Admin
    '''

    def label_from_instance(self, obj):
        return "%s" % (obj.full_name)


def form_view(some_func):
    def inner(*args, **kwargs):
        dct = some_func(args, kwargs)
        request = (args)[0]
        id = kwargs.get('id')
        if id:
            obj = get_object_or_404(dct['model'], id=id)
            scenario = 'Update'
        else:
            obj = dct['model']()
            scenario = 'Create'
        if request.POST:
            form = dct['form'](data=request.POST, instance=obj)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.save()
                if request.is_ajax():
                    return render(request, 'callback.html', {'obj': dct['serializer'](obj).data})
                return redirect(reverse(dct['listing_url']))
        else:
            form = dct['form'](instance=obj)
        if request.is_ajax():
            base_template = 'modal.html'
        else:
            base_template = 'base.html'
        return render(request, dct['template'], {
            'scenario': scenario,
            'form': form,
            'base_template': base_template,
        })

    return inner


# class MultilingualQuerySet(models.query.QuerySet):
# selected_language = None
#
# def __init__(self, *args, **kwargs):
# super(MultilingualQuerySet, self).__init__(*args, **kwargs)
#
#     def select_language(self, lang):
#         if not lang:
#             lang = translation.get_language()
#             # e.g. en-us to en
#             lang = lang.split('-')[0]
#         self.selected_language = lang
#         return self
#
#     def iterator(self):
#         result_iter = super(MultilingualQuerySet, self).iterator()
#         for result in result_iter:
#             if hasattr(result, 'select_language'):
#                 result.select_language(self.selected_language)
#             yield result
#
#     def _clone(self, *args, **kwargs):
#         qs = super(MultilingualQuerySet, self)._clone(*args, **kwargs)
#         if hasattr(qs, 'select_language'):
#             qs.select_language(self.selected_language)
#         return qs
#
#
# class MultilingualManager(models.Manager):
#     use_for_related_fields = True
#     selected_language = None
#
#     def select_language(self, lang):
#         self.selected_language = lang
#         return self
#
#     def get_queryset(self):
#         qs = MultilingualQuerySet(self.model, using=self._db)
#         return qs.select_language(self.selected_language)
#
#
# class MultilingualModel(models.Model):
#     # fallback/default language code
#     default_language = 'en'
#
#     # currently selected language
#     selected_language = None
#
#     class Meta:
#         abstract = True
#
#     def select_language(self, lang):
#         """Select a language"""
#         # import pdb
#         # pdb.set_trace()
#         self.selected_language = lang
#         return self
#
#     objects = MultilingualManager()
#
#     def __getattribute__(self, name):
#         def get(x):
#             return super(MultilingualModel, self).__getattribute__(x)
#
#         try:
#             # Try to get the original field, if exists
#             value = get(name)
#             # If we can select language on the field as well, do it
#             if isinstance(value, MultilingualModel):
#                 value.select_language(get('selected_language'))
#             return value
#         except AttributeError, e:
#             # Try the translated variant, falling back to current language if no
#             # language has been explicitly selected
#             lang = translation.get_language()
#             # e.g. en-us to en
#             lang = lang.split('-')[0]
#             if not lang:
#                 lang = self.default_language
#             if not lang:
#                 raise
#
#             value = get(name + '_' + lang)
#
#             # If the translated variant is empty, fallback to default
#             if isinstance(value, basestring) and value == u'':
#                 value = get(name + '_' + self.default_language)
#                 # if value is still u'', look for values in other languages
#                 if value == u'':
#                     fields = [getattr(field, 'name') for field in self._meta.fields if
#                               getattr(field, name).startswith(name + '_')]
#                     for field in fields:
#                         value = getattr(self, field)
#                         if value != u'':
#                             break
#
#         if type(value) == unicode:
#             return value.encode('utf-8')
#         return value
#
#
# class MultiNameModel(MultilingualModel):
#     name_ne = models.CharField(max_length=254, verbose_name=_('Name in Nepali'), blank=True, null=True)
#     name_en = models.CharField(max_length=254, verbose_name=_('Name in English'), blank=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         abstract = True

class NameTranslationOptions(TranslationOptions):
    fields = ('name',)


from modeltranslation.admin import TranslationAdmin as BaseTranslationAdmin, deepcopy, ClearableWidgetWrapper, \
    build_css_class


class TranslationAdmin(BaseTranslationAdmin):
    def patch_translation_field(self, db_field, field, **kwargs):
        if db_field.name in self.trans_opts.fields:
            if field.required:
                field.required = False
                field.blank = True
                self._orig_was_required['%s.%s' % (db_field.model._meta, db_field.name)] = True
        try:
            orig_field = db_field.translated_field
        except AttributeError:
            pass
        else:
            orig_formfield = self.formfield_for_dbfield(orig_field, **kwargs)
            field.widget = deepcopy(orig_formfield.widget)
            if orig_field.name in self.both_empty_values_fields:
                from modeltranslation.forms import NullableField, NullCharField

                form_class = field.__class__
                if issubclass(form_class, NullCharField):
                    # NullableField don't work with NullCharField
                    form_class.__bases__ = tuple(
                        b for b in form_class.__bases__ if b != NullCharField)
                field.__class__ = type(
                    'Nullable%s' % form_class.__name__, (NullableField, form_class), {})
            if ((db_field.empty_value == 'both' or orig_field.name in self.both_empty_values_fields)
                and isinstance(field.widget, (forms.TextInput, forms.Textarea))):
                field.widget = ClearableWidgetWrapper(field.widget)
            css_classes = field.widget.attrs.get('class', '').split(' ')
            css_classes.append('mt')
            css_classes.append(build_css_class(db_field.name, 'mt-field'))

            from django.utils.translation import get_language

            if db_field.language == get_language():
                css_classes.append('mt-default')
                if (orig_formfield.required or self._orig_was_required.get(
                            '%s.%s' % (orig_field.model._meta, orig_field.name))):
                    orig_formfield.required = False
                    orig_formfield.blank = True
                    field.required = True
                    field.blank = False
                    if isinstance(field.widget, ClearableWidgetWrapper):
                        field.widget = field.widget.widget
            field.widget.attrs['class'] = ' '.join(css_classes)


def title_case(line):
    return ' '.join([s[0].upper() + s[1:] for s in line.split(' ')])
