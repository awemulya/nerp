from django.shortcuts import render, redirect
from django.contrib.auth.views import login
from django.contrib.auth import logout as auth_logout


def index(request):
    if request.user.is_authenticated():
        context = {}
        try:
            from project.models import Project

            context['projects'] = Project.objects.filter(active=True)
        except ImportError:
            pass
        return render(request, 'dashboard_index.html', context)
    return login(request)


def web_login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('/', **kwargs)
    else:
        if request.method == 'POST':
            if request.POST.has_key('remember_me'):
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)
        return login(request, **kwargs)


def logout(request, next_page=None):
    auth_logout(request)
    if next_page:
        return redirect(next_page)
    return redirect('/')
