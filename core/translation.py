from modeltranslation.translator import translator
from app.utils.translation import NameTranslationOptions
from .models import Donor, Activity, BudgetHead, Employee, TaxScheme

translator.register(Donor, NameTranslationOptions)
translator.register(Activity, NameTranslationOptions)
translator.register(BudgetHead, NameTranslationOptions)
translator.register(Employee, NameTranslationOptions)
translator.register(TaxScheme, NameTranslationOptions)