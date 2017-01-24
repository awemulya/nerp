from modeltranslation.translator import translator, TranslationOptions
from app.utils.translation import NameTranslationOptions
from hr.models import Employee, DeductionName, BranchOffice, IncentiveName, AllowanceName, Designation, \
    EmployeeGradeGroup, EmployeeGrade


class DesignationTranslationOptions(TranslationOptions):
    fields = ('designation_name',)


class EmployeeGradeTranslationOptions(TranslationOptions):
    fields = ('grade_name',)


translator.register(Employee, NameTranslationOptions)
translator.register(DeductionName, NameTranslationOptions)
translator.register(BranchOffice, NameTranslationOptions)
translator.register(IncentiveName, NameTranslationOptions)
translator.register(AllowanceName, NameTranslationOptions)
translator.register(EmployeeGradeGroup, NameTranslationOptions)
translator.register(Designation, DesignationTranslationOptions)
translator.register(EmployeeGrade, EmployeeGradeTranslationOptions)
