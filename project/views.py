import json

from core.serializers import BudgetSerializer
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView
from app.utils.helpers import save_model, invalid, empty_to_none
from core.models import FiscalYear, BudgetHead
from inventory.models import delete_rows
from models import Aid, BudgetAllocationItem, BudgetReleaseItem, Expenditure
from project.forms import AidForm, ProjectForm, ExpenseCategoryForm, ExpenseForm
from models import ImprestTransaction, ExpenseRow, ExpenseCategory, Expense, Project
from serializers import ImprestTransactionSerializer, ExpenseRowSerializer, ExpenseCategorySerializer, \
    ExpenseSerializer, \
    AidSerializer, BaseStatementSerializer
from app.utils.mixins import AjaxableResponseMixin, UpdateView, ProjectCreateView as CreateView, DeleteView


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


class ProjectMixin(object):
    def get_queryset(self):
        queryset = super(ProjectMixin, self).get_queryset()
        if 'project_id' in self.kwargs:
            queryset = self.model.objects.filter(project_id=self.kwargs['project_id'])
        return queryset

    def form_valid(self, form):
        form.instance.project = Project.objects.get(pk=self.kwargs['project_id'])
        super(ProjectMixin, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        super(ProjectMixin, self).post(request, *args, **kwargs)
        return HttpResponseRedirect(reverse(self.success_url, kwargs={'project_id': self.kwargs['project_id']}))


class AidView(ProjectView, ProjectMixin):
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


class ExpenseCategoryView(ProjectView, ProjectMixin):
    model = ExpenseCategory
    success_url = 'expense_category_list'
    form_class = ExpenseCategoryForm


class ExpenseCategoryList(ExpenseCategoryView, ListView):
    pass


class ExpenseCategoryCreate(AjaxableResponseMixin, ExpenseCategoryView, CreateView):
    pass


class ExpenseCategoryUpdate(ExpenseCategoryView, UpdateView):
    pass


class ExpenseCategoryDelete(ExpenseCategoryView, DeleteView):
    pass


class ExpenseView(ProjectView, ProjectMixin):
    model = Expense
    success_url = 'expense_list'
    form_class = ExpenseForm

    def get_context_data(self, **kwargs):
        context_data = super(ExpenseView, self).get_context_data(**kwargs)
        if 'form' in context_data:
            project_id = context_data['project'].id
            form = context_data['form']
            form.fields['category'].queryset = ExpenseCategory.objects.filter(project_id=project_id)
        return context_data


class ExpenseList(ExpenseView, ListView):
    pass


class ExpenseCreate(AjaxableResponseMixin, ExpenseView, CreateView):
    pass


class ExpenseUpdate(ExpenseView, UpdateView):
    pass


class ExpenseDelete(ExpenseView, DeleteView):
    pass


class BaseStatement(object):
    def get_fy(self):
        if not self.fy:
            self.fy = FiscalYear.get()
        return self.fy

    def get_context_data(self, **kwargs):
        context_data = super(BaseStatement, self).get_context_data(**kwargs)
        budget_head = BudgetHead.objects.all()
        aid = Aid.objects.filter(active=True, project=context_data['project'].id)
        context_data['data'] = {
            'fy': self.get_fy().id,
            'project_id': context_data['project'].id,
            'rows': BaseStatementSerializer(context_data['object_list'], many=True).data,
            'budget_head': BudgetSerializer(budget_head, many=True).data,
            'aid': AidSerializer(aid, many=True).data,
        }
        return context_data

    def get_queryset(self):
        return self.model.objects.filter(project_id=self.kwargs['project_id'])


def base_save(request, model):
    params = json.loads(request.body)
    fy = params.get('fy')
    project_id = params.get('project_id')
    dct = {'rows': {}}
    model = model
    try:
        for index, row in enumerate(params.get('table_view').get('rows')):
            if invalid(row, ['budget_head_id']):
                continue
            values = {'budget_head_id': row.get('budget_head_id'),
                      'fy_id': fy, 'project_id': project_id}
            dct['rows'][index] = {}
            if row.get('goa_id') or row.get('goa_amount'):
                values['amount'] = empty_to_none(row.get('goa_amount'))
                submodel, created = model.objects.get_or_create(id=row.get('goa_id'), defaults=values)
                if not created:
                    submodel = save_model(submodel, values)
                if not row.get('goa_amount') and row.get('goa_id'):
                    model.objects.get(id=row.get('goa_id')).delete()
                dct['rows'][index]['goa_id'] = submodel.id
            for aid in params.get('count'):
                if row.get(aid) or row.get(aid + '-id'):
                    values['aid_id'] = aid.split('-')[0]
                    values['amount'] = empty_to_none(row.get(aid))
                    submodel, created = model.objects.get_or_create(id=row.get(aid + '-id'), defaults=values)
                    if not created:
                        submodel = save_model(submodel, values)
                    if not row.get(aid) and row.get(aid + '-id'):
                        model.objects.get(id=row.get(aid + '-id')).delete()
                    dct['rows'][index][aid + '-id'] = submodel.id
    except Exception as e:
        if hasattr(e, 'messages'):
            dct['error_message'] = '; '.join(e.messages)
        elif str(e) != '':
            dct['error_message'] = str(e)
        else:
            dct['error_message'] = 'Error in form data!'
    delete_budget_allocation(params.get('table_view').get('deleted_rows'), model)
    return JsonResponse(dct)


def delete_budget_allocation(rows, model):
    for row in rows:
        # ipdb.set_trace()
        for o in row.get('aid_amount'):
            if o.get('id'):
                try:
                    instance = model.objects.get(id=o.get('id'))
                    instance.delete()
                except:
                    pass
        if row.get('goa_id'):
            try:
                instance = model.objects.get(id=row.get('goa_id'))
                instance.delete()
            except:
                pass


class BudgetAllocaionCreate(BaseStatement, ProjectView, ListView):
    model = BudgetAllocationItem
    fy = None


@login_required
def save_budget_allocation(request):
    return base_save(request, BudgetAllocationItem)


class BudgetReleaseCreate(BaseStatement, ProjectView, ListView):
    model = BudgetReleaseItem
    fy = None


@login_required
def save_budget_release(request):
    import ipdb
    ipdb.set_trace()
    return base_save(request, BudgetReleaseItem)


class ExpenditureCreate(BaseStatement, ProjectView, ListView):
    model = Expenditure
    fy = None
    template_name = 'project/expenditure_list.html'

    def get_queryset(self):
        if not self.model.objects.filter(project_id=self.kwargs['project_id']):
            return BudgetReleaseItem.objects.filter(project_id=self.kwargs['project_id'])
        return self.model.objects.filter(project_id=self.kwargs['project_id'])


@login_required
def save_expenditure(request):
    import ipdb
    # ipdb.set_trace()
    return base_save(request, Expenditure)
