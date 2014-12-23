# -*- coding: utf-8 -*-

from django.utils import translation
from modeltranslation.translator import TranslationOptions
from modeltranslation.admin import TranslationAdmin as BaseTranslationAdmin, deepcopy, ClearableWidgetWrapper, \
    build_css_class
from django import forms
import re
import datetime


def ne2en(num, reverse=False):
    if num is None:
        return None
    dct = {
        u'०': '0',
        u'१': '1',
        u'२': '2',
        u'३': '3',
        u'४': '4',
        u'५': '5',
        u'६': '6',
        u'७': '7',
        u'८': '8',
        u'९': '9'
    }
    if reverse:
        dct = dict((v, k) for k, v in dct.iteritems())
    pattern = re.compile('|'.join(dct.keys()))
    grouper = lambda x: dct[x.group()]
    num = unicode(num)
    result = pattern.sub(grouper, num)
    return result

    # devanagari_nums = (u'०', u'१', u'२', u'३', u'४', u'५', u'६', u'७', u'८', u'९')
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


class NameTranslationOptions(TranslationOptions):
    fields = ('name',)


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


from django.db.models.fields import DateField
from django.forms.fields import DateField as DateFormField
from django.core import exceptions
from django.db import models
import nepdate


class BSDateFormField(DateFormField):
    def __init__(self, *args, **kwargs):
        super(BSDateFormField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if nepdate.is_valid(value):
            return value
        else:
            raise exceptions.ValidationError(
                self.default_error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )


class BSDateField(DateField):
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return "DateField"

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, datetime.datetime):
            # TODO Timezone Awareness
            return nepdate.string_from_tuple(nepdate.ad2bs(value.date()))
        if isinstance(value, datetime.date):
            return nepdate.string_from_tuple(nepdate.ad2bs(value))
        return value

    def pre_save(self, model_instance, add):
        return nepdate.bs2ad(self._get_val_from_obj(model_instance))

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return unicode(value)

    def formfield(self, **kwargs):
        defaults = {'form_class': BSDateFormField}
        defaults.update(kwargs)
        return super(DateField, self).formfield(**defaults)