from django.shortcuts import render
from django.views.generic import ListView

from core.models import FiscalYear
from project.models import ImprestTransaction


def imprest_ledger(request):
    context = {
        'fy': FiscalYear.get()
    }
    return render(request, 'imprest_ledger.html', context)


class ImprestLedger(ListView):
    model = ImprestTransaction
    template_name = 'imprest_ledger.html'
    fy = None

    def get_fy(self):
        if not self.fy:
            self.fy = FiscalYear.get()
        return self.fy

    def get_context_data(self, **kwargs):
        context_data = super(ImprestLedger, self).get_context_data(**kwargs)
        context_data['fy'] = self.get_fy()
        return context_data

    def get_queryset(self):
        qs = super(ImprestLedger, self).get_queryset()
        qs.filter(fy=self.get_fy())
        return qs
