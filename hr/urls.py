from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^$', views.payroll_entry, name='payroll_entry'),
                       url(r'^test/$', views.test, name='test'),
                       url(r'^get_employee_account/$', views.get_employee_account, name='get_employee_account'),
                       url(r'^get_employees_account/$', views.get_employees_account, name='get_employees_account'),
                       url(r'^save_payroll_entry/$', views.save_payroll_entry, name='save_payroll_entry'),
                       url(r'^entry_detail/(?P<pk>[0-9]+)/$', views.entry_detail, name='entry_detail'),
                       url(r'^entry_list/$', views.entry_list, name='entry_list'),
                       url(r'^get_employee_options/$', views.get_employee_options, name='get_employee_options'),
                       url(r'^approve_entry/(?P<pk>[0-9]+)/$', views.approve_entry, name='approve_entry'),
                       url(r'^transact_entry/(?P<pk>[0-9]+)/$', views.transact_entry, name='transact_entry'),
                       url(r'^delete_entry/(?P<pk>[0-9]+)/$', views.delete_entry, name='delete_entry'),

                       # employee crud
                       url(r'^employee/add/$', views.employee, name='employee_add'),
                       url(r'^employee/edit/(?P<pk>[0-9]+)/$', views.employee, name='edit_employee'),
                       url(r'^employee/delete/(?P<pk>[0-9]+)/$', views.delete_employee, name='delete_employee'),
                       url(r'^employee/list/$', views.list_employee, name='list_employee'),

                       # incentive crud
                       url(r'^incentive/add/$', views.incentive, name='add_incentive'),
                       url(r'^incentive/edit/(?P<pk>[0-9]+)/$', views.incentive, name='edit_incentive'),
                       url(r'^incentive/delete/(?P<pk>[0-9]+)/$', views.delete_incentive, name='delete_incentive'),
                       url(r'^incentive/list/$', views.list_incentive, name='list_incentive'),

                       # allowance crud
                       url(r'^allowance/add/$', views.allowance, name='add_allowance'),
                       url(r'^allowance/edit/(?P<pk>[0-9]+)/$', views.allowance, name='edit_allowance'),
                       url(r'^allowance/delete/(?P<pk>[0-9]+)/$', views.delete_allowance, name='delete_allowance'),
                       url(r'^allowance/list/$', views.list_allowance, name='list_allowance'),

                       # deductions crud
                       url(r'^deduction/$', views.deduction, name='deduction'),
                       # url(r'^allowance/edit/(?P<pk>[0-9]+)/$', views.allowance, name='edit_allowance'),
                       # url(r'^by_branch/$', views.group_payroll_branch, name='group_payroll_branch'),
                       )
