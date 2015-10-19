from django import http
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.http import is_safe_url
from django.contrib.auth.decorators import user_passes_test

from account.serializers import AccountSerializer
from app.utils.forms import form_view
from core.forms import PartyForm, EmployeeForm
from core.models import Party, Employee, BudgetHead, Donor, Activity, Account, TaxScheme, Language, FISCAL_YEARS, FiscalYear
from core.serializers import PartySerializer, EmployeeSerializer, BudgetSerializer, ActivitySerializer, DonorSerializer, \
    TaxSchemeSerializer, LanguageSerializer
from users.models import group_required
from .signals import fiscal_year_signal


@group_required('Store Keeper', 'Chief', 'Accountant')
def list_parties(request):
    objects = Party.objects.all()
    return render(request, 'list_parties.html', {'objects': objects})


@group_required('Store Keeper', 'Chief', 'Accountant')
def party_form(request, id=None):
    if id:
        obj = get_object_or_404(Party, id=id)
        scenario = 'Update'
    else:
        obj = Party()
        scenario = 'Create'
    if request.POST:
        form = PartyForm(data=request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            if request.is_ajax():
                return render(request, 'callback.html', {'obj': PartySerializer(obj).data})
            return redirect(reverse('list_parties'))
    else:
        form = PartyForm(instance=obj)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'base.html'
    return render(request, 'party_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': base_template,
    })


@group_required('Store Keeper', 'Chief', 'Accountant')
def delete_party(request, id):
    obj = get_object_or_404(Party, id=id)
    obj.delete()
    return redirect(reverse('list_parties'))


@group_required('Store Keeper', 'Chief', 'Accountant')
def parties_as_json(request):
    objects = Party.objects.all()
    objects_data = PartySerializer(objects, many=True).data
    return JsonResponse(objects_data, safe=False)


@group_required('Store Keeper', 'Chief', 'Accountant')
def list_employees(request):
    objects = Employee.objects.all()
    return render(request, 'list_employees.html', {'objects': objects})


@group_required('Store Keeper', 'Chief', 'Accountant')
@form_view
def employee_form(request, id=None):
    return {
        'model': Employee,
        'form': EmployeeForm,
        'serializer': EmployeeSerializer,
        'listing_url': 'list_employees',
        'template': 'employee_form.html'
    }


@group_required('Store Keeper', 'Chief', 'Accountant')
def delete_employee(request, id):
    obj = get_object_or_404(Employee, id=id)
    obj.delete()
    return redirect(reverse('list_employees'))


@group_required('Store Keeper', 'Chief', 'Accountant')
def employees_as_json(request):
    objects = Employee.objects.all()
    objects_data = EmployeeSerializer(objects).data
    return JsonResponse(objects_data, safe=False)


def budget_heads_as_json(request):
    objects = BudgetHead.objects.all()
    objects_data = BudgetSerializer(objects, many=True).data
    return JsonResponse(objects_data, safe=False)


def donors_as_json(request):
    objects = Donor.objects.all()
    objects_data = DonorSerializer(objects, many=True).data
    return JsonResponse(objects_data, safe=False)


def activities_as_json(request):
    objects = Activity.objects.all()
    objects_data = ActivitySerializer(objects, many=True).data
    return JsonResponse(objects_data, safe=False)


def accounts_as_json(request):
    objects = Account.objects.all()
    objects_data = AccountSerializer(objects, many=True).data
    return JsonResponse(objects_data, safe=False)


def tax_schemes_as_json(request):
    objects = TaxScheme.objects.all()
    objects_data = TaxSchemeSerializer(objects, many=True).data
    return JsonResponse(objects_data, safe=False)


def languages_as_json(request):
    objects = Language.objects.all()
    objects_data = LanguageSerializer(objects, many=True).data
    return JsonResponse(objects_data, safe=False)


def change_calendar(request):
    nxt = request.POST.get('next', request.GET.get('next'))
    if not is_safe_url(url=nxt, host=request.get_host()):
        nxt = request.META.get('HTTP_REFERER')
        if not is_safe_url(url=nxt, host=request.get_host()):
            nxt = '/'
    response = http.HttpResponseRedirect(nxt)
    if request.method == 'POST':
        cal_code = request.POST.get('calendar')
        if cal_code and hasattr(request, 'session'):
            request.session['sess_cal'] = cal_code
    return response


@user_passes_test(lambda u: u.is_superuser)
def change_fiscal_year(request):
    if request.POST:
        new_fiscal_year_str = request.POST.get('fiscal_year')

        # app_setting.fiscal_year = new_fiscal_year_str
        from dbsettings.models import Setting

        fiscal_year_setting = Setting.objects.get(module_name='core.models', attribute_name='fiscal_year')
        fiscal_year_setting.value = new_fiscal_year_str
        fiscal_year_setting.save()

        old_fiscal_year = FiscalYear.get()
        new_fiscal_year = FiscalYear.get(new_fiscal_year_str)
        fiscal_year_signal.send(sender=None, new_fiscal_year_str=new_fiscal_year_str, old_fiscal_year=old_fiscal_year,
                                new_fiscal_year=new_fiscal_year)

    context = {
        'has_permission': True, # required for user tools to show at admin
        'fiscal_years': FISCAL_YEARS,
        'current_fiscal_year': FiscalYear.get()
    }
    return render(request, 'change_fiscal_year.html', context)
