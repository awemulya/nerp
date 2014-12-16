from django.utils import translation
from django.db import models
from django.utils.translation import ugettext_lazy as _


class MultilingualQuerySet(models.query.QuerySet):
    selected_language = None

    def __init__(self, *args, **kwargs):
        super(MultilingualQuerySet, self).__init__(*args, **kwargs)

    def select_language(self, lang):
        if not lang:
            lang = translation.get_language()
            # e.g. en-us to en
            lang = lang.split('-')[0]
        self.selected_language = lang
        return self

    def iterator(self):
        result_iter = super(MultilingualQuerySet, self).iterator()
        for result in result_iter:
            if hasattr(result, 'select_language'):
                result.select_language(self.selected_language)
            yield result

    def _clone(self, *args, **kwargs):
        qs = super(MultilingualQuerySet, self)._clone(*args, **kwargs)
        if hasattr(qs, 'select_language'):
            qs.select_language(self.selected_language)
        return qs


class MultilingualManager(models.Manager):
    use_for_related_fields = True
    selected_language = None

    def select_language(self, lang):
        self.selected_language = lang
        return self

    def get_queryset(self):
        qs = MultilingualQuerySet(self.model, using=self._db)
        return qs.select_language(self.selected_language)


class MultilingualModel(models.Model):
    # fallback/default language code
    default_language = 'en'

    # currently selected language
    selected_language = None

    class Meta:
        abstract = True

    def select_language(self, lang):
        """Select a language"""
        # import pdb
        # pdb.set_trace()
        self.selected_language = lang
        return self

    objects = MultilingualManager()

    def __getattribute__(self, name):
        def get(x):
            return super(MultilingualModel, self).__getattribute__(x)

        try:
            # Try to get the original field, if exists
            value = get(name)
            # If we can select language on the field as well, do it
            if isinstance(value, MultilingualModel):
                value.select_language(get('selected_language'))
            return value
        except AttributeError, e:
            # Try the translated variant, falling back to current language if no
            # language has been explicitly selected
            lang = translation.get_language()
            # e.g. en-us to en
            lang = lang.split('-')[0]
            if not lang:
                lang = self.default_language
            if not lang:
                raise

            value = get(name + '_' + lang)

            # If the translated variant is empty, fallback to default
            if isinstance(value, basestring) and value == u'':
                value = get(name + '_' + self.default_language)
                # if value is still u'', look for values in other languages
                if value == u'':
                    fields = [getattr(field, 'name') for field in self._meta.fields if
                              getattr(field, name).startswith(name + '_')]
                    for field in fields:
                        value = getattr(self, field)
                        if value != u'':
                            break

        if type(value) == unicode:
            return value.encode('utf-8')
        return value


class MultiNameModel(MultilingualModel):
    name_ne = models.CharField(max_length=254, verbose_name=_('Name in Nepali'), blank=True, null=True)
    name_en = models.CharField(max_length=254, verbose_name=_('Name in English'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
