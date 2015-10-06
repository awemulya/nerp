# -*- coding: utf-8 -*-

from modeltranslation.translator import TranslationOptions
from modeltranslation.admin import TranslationAdmin as BaseTranslationAdmin, deepcopy, ClearableWidgetWrapper, \
    build_css_class
from django import forms

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


