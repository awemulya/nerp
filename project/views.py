import json

from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView
from app.utils.helpers import save_model, invalid
from core.models import FiscalYear
from inventory.models import delete_rows
from models import Aid
from project.forms import AidForm, ProjectForm, ExpenseCategoryForm, ExpenseForm
from models import ImprestTransaction, ExpenseRow, ExpenseCategory, Expense, Project
from serializers import ImprestTransactionSerializer, ExpenseRowSerializer, ExpenseCategorySerializer, ExpenseSerializer
from app.utils.mixins import AjaxableResponseMixin, UpdateView, CreateView, DeleteView


class ProjectView(object):
    fy = None

    def get_fy(self):
        if not self.fy:
            self.fy = FiscalYear.get()
        return self.fy

    def get_context_data(self, **kwargs):
        context_data = super(ProjectView, self).get_context_data(**kwargs)
        context_data['fy'] = self.get_fy()
        if 'data' in context_data:
            context_data['data']['fy_id'] = context_data['fy'].id,
        if 'project_id' in self.kwargs:
            try:
                context_data['project'] = Project.objects.get(pk=self.kwargs.pop('project_id'), active=True)
                if 'data' in context_data:
                    context_data['data']['project_id'] = context_data['project'].id,
            except Project.DoesNotExist:
                pass

        return context_data


def index(request):
    projects = Project.objects.filter(active=True)
    return render(request, 'project_index.html', {'projects': projects})


def imprest_ledger(request, project_id):
    project = Project.objects.get(pk=project_id)
    context = {
        'fy': FiscalYear.get(),
        'project': project,
    }
    return render(request, 'imprest_ledger.html', context)


class ImprestLedger(ProjectView, ListView):
    model = ImprestTransaction
    template_name = 'imprest_ledger.html'
    fy = None

    def get_context_data(self, **kwargs):
        context_data = super(ImprestLedger, self).get_context_data(**kwargs)
        context_data['data'] = {
            'rows': ImprestTransactionSerializer(context_data['object_list'], many=True).data,
        }
        return context_data

    def get_queryset(self):
        qs = super(ImprestLedger, self).get_queryset()
        qs = qs.filter(fy=self.get_fy())
        return qs


@login_required
def save_imprest_ledger(request):
    params = json.loads(request.body)
    dct = {'rows': {}}
    model = ImprestTransaction
    fy_id = params.get('fy_id')
    try:
        for index, row in enumerate(params.get('table_view').get('rows')):
            if invalid(row, ['date']):
                continue
            values = {'date': row.get('date', ''),
                      'name': row.get('name'),
                      'type': row.get('type'),
                      'date_of_payment': row.get('date_of_payment', ''),
                      'wa_no': row.get('wa_no'),
                      'amount_nrs': row.get('amount_nrs', None),
                      'amount_usd': row.get('amount_usd', None),
                      'exchange_rate': row.get('exchange_rate', None),
                      'fy_id': fy_id
                      }
            submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
            if not created:
                submodel = save_model(submodel, values)
            dct['rows'][index] = submodel.id
    except Exception as e:
        if hasattr(e, 'messages'):
            dct['error_message'] = '; '.join(e.messages)
        elif str(e) != '':
            dct['error_message'] = str(e)
        else:
            dct['error_message'] = 'Error in form data!'
    delete_rows(params.get('table_view').get('deleted_rows'), model)
    return JsonResponse(dct)


class Application(ListView):
    model = ExpenseRow
    template_name = 'application.html'
    fy = None

    def get_fy(self):
        if not self.fy:
            self.fy = FiscalYear.get()
        return self.fy

    def get_context_data(self, **kwargs):
        context_data = super(Application, self).get_context_data(**kwargs)
        context_data['fy'] = self.get_fy()
        categories = ExpenseCategory.objects.filter(enabled=True)
        expenses = Expense.objects.filter(enabled=True)
        context_data['data'] = {
            'fy_id': self.get_fy().id,
            'rows': ExpenseRowSerializer(context_data['object_list'], many=True).data,
            'categories': ExpenseCategorySerializer(categories, many=True).data,
            'expenses': ExpenseSerializer(expenses, many=True).data,
        }
        return context_data

    def get_queryset(self):
        qs = super(Application, self).get_queryset()
        qs = qs.filter(fy=self.get_fy())
        return qs


@login_required
def save_application(request):
    params = json.loads(request.body)
    dct = {'categories': {}}
    model = ExpenseRow
    fy_id = params.get('fy_id')
    try:
        for cat_index, category in enumerate(params.get('categories')):
            dct['categories'][cat_index] = {'rows': {}}
            for index, row in enumerate(category.get('rows')):
                if invalid(row, ['category_id', 'expense_id', 'amount']):
                    continue
                values = {'category_id': row.get('category_id'),
                          'expense_id': row.get('expense_id'),
                          'amount': row.get('amount'),
                          'fy_id': fy_id
                          }
                submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
                if not created:
                    submodel = save_model(submodel, values)
                dct['categories'][cat_index]['rows'][index] = submodel.id
            delete_rows(category.get('deleted_rows'), model)
    except Exception as e:
        if hasattr(e, 'messages'):
            dct['error_message'] = '; '.join(e.messages)
        elif str(e) != '':
            dct['error_message'] = str(e)
        else:
            dct['error_message'] = 'Error in form data!'
    # delete_rows(params.get('table_view').get('deleted_rows'), model)
    return JsonResponse(dct)


class ProjectListCreateMixin(object):
    def get_queryset(self):
        queryset = super(ProjectListCreateMixin, self).get_queryset()
        if 'project_id' in self.kwargs:
            queryset = self.model.objects.filter(project_id=self.kwargs['project_id'])
        return queryset

    def form_valid(self, form):
        form.instance.project = Project.objects.get(pk=self.kwargs['project_id'])
        super(ProjectListCreateMixin, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        super(ProjectListCreateMixin, self).post(request, *args, **kwargs)
        return HttpResponseRedirect(reverse(self.success_url, kwargs={'project_id': self.kwargs['project_id']}))


class AidView(ProjectView, ProjectListCreateMixin):
    model = Aid
    success_url = 'aid_list'
    form_class = AidForm


class AidList(AidView, ListView):
    pass


class AidCreate(AjaxableResponseMixin, AidView, CreateView):
    pass


class AidUpdate(AidView, UpdateView):
    pass


class AidDelete(AidView, DeleteView):
    pass


class ProjectAppView(object):
    model = Project
    success_url = reverse_lazy('project_list')
    form_class = ProjectForm


class ProjectList(ProjectAppView, ListView):
    pass


class ProjectCreate(AjaxableResponseMixin, ProjectAppView, CreateView):
    pass


class ProjectUpdate(ProjectAppView, UpdateView):
    pass


class ProjectDelete(ProjectAppView, DeleteView):
    pass


class ExpenseCategoryView(object):
    model = ExpenseCategory
    success_url = reverse_lazy('expense_category_list')
    form_class = ExpenseCategoryForm


class ExpenseCategoryList(ExpenseCategoryView, ListView):
    pass


class ExpenseCategoryCreate(AjaxableResponseMixin, ExpenseCategoryView, CreateView):
    pass


class ExpenseCategoryUpdate(ExpenseCategoryView, UpdateView):
    pass


class ExpenseCategoryDelete(ExpenseCategoryView, DeleteView):
    pass


class ExpenseView(object):
    model = Expense
    success_url = reverse_lazy('expense_list')
    form_class = ExpenseForm


class ExpenseList(ExpenseView, ListView):
    pass


class ExpenseCreate(AjaxableResponseMixin, ExpenseView, CreateView):
    pass


class ExpenseUpdate(ExpenseView, UpdateView):
    pass


class ExpenseDelete(ExpenseView, DeleteView):
    pass
