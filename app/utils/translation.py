# -*- coding: utf-8 -*-

from django.utils import translation
from modeltranslation.translator import TranslationOptions
from modeltranslation.admin import TranslationAdmin as BaseTranslationAdmin, deepcopy, ClearableWidgetWrapper, \
    build_css_class
from django import forms
import re


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