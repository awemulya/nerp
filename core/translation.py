from modeltranslation.translator import translator
from app.utils.translation import NameTranslationOptions
from .models import Party, Donor, Activity, BudgetHead, Employee, TaxScheme

translator.register(Party, NameTranslationOptions)
translator.register(Donor, NameTranslationOptions)
translator.register(Activity, NameTranslationOptions)
translator.register(BudgetHead, NameTranslationOptions)
translator.register(Employee, NameTranslationOptions)
translator.register(TaxScheme, NameTranslationOptions)