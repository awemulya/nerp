from django.shortcuts import render


# Create your views here.
def payroll_entry(request):
    return render(request, 'payroll_entry.html', {'form': 6})
