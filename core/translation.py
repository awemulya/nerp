from modeltranslation.translator import translator, TranslationOptions
from app.libr import NameTranslationOptions
from .models import Party, Donor, Activity, BudgetHead, Account, Employee, TaxScheme

translator.register(Party, NameTranslationOptions)
translator.register(Donor, NameTranslationOptions)
translator.register(Activity, NameTranslationOptions)
translator.register(BudgetHead, NameTranslationOptions)
translator.register(Account, NameTranslationOptions)
translator.register(Employee, NameTranslationOptions)
translator.register(TaxScheme, NameTranslationOptions)