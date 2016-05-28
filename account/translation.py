from modeltranslation.translator import translator
from app.utils.translation import NameTranslationOptions
from account.models import Party

translator.register(Party, NameTranslationOptions)
