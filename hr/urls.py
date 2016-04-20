from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^$', views.payroll_entry, name='payroll_entry'),
                       url(r'^test/$', views.test, name='test'),
                       url(r'^get_employee_account/$', views.get_employee_account, name='get_employee_account'),
                       url(r'^get_employees_account/$', views.get_employees_account, name='get_employees_account'),
                       # url(r'^by_branch/$', views.group_payroll_branch, name='group_payroll_branch'),
                       )
