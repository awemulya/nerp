from django.shortcuts import render
from .forms import PaymentRowForm, PayrollEntryForm

# Create your views here.
def payroll_entry(request):
    form = PaymentRowForm()
    return render(request, 'payroll_entry.html', {'form': form})
