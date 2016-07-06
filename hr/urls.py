from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^$', views.payroll_entry, name='payroll_entry'),
                       url(r'^(?P<pk>[0-9]+)/$', views.payroll_entry, name='payroll_entry'),
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
                       url(r'^employee/add/$', views.employee, name='add_employee'),
                       url(r'^employee/edit/(?P<pk>[0-9]+)/$', views.employee, name='edit_employee'),
                       url(r'^employee/toggle_activeness/(?P<pk>[0-9]+)/$', views.toggle_employee_activeness, name='toggle_employee_activeness'),
                       url(r'^employee/list/$', views.list_employee, name='list_employee'),

                       # # incentive crud
                       # url(r'^incentive/add/$', views.incentive, name='add_incentive'),
                       # url(r'^incentive/edit/(?P<pk>[0-9]+)/$', views.incentive, name='edit_incentive'),
                       # url(r'^incentive/delete/(?P<pk>[0-9]+)/$', views.delete_incentive, name='delete_incentive'),
                       # url(r'^incentive/list/$', views.list_incentive, name='list_incentive'),

                       # allowance crud
                       url(r'^allowance/add/$', views.allowance, name='add_allowance'),
                       url(r'^allowance/edit/(?P<pk>[0-9]+)/$', views.allowance, name='edit_allowance'),
                       url(r'^allowance/delete/(?P<pk>[0-9]+)/$', views.delete_allowance, name='delete_allowance'),
                       url(r'^allowance/list/$', views.list_allowance, name='list_allowance'),

                       # deductions crud
                       url(r'^deduction/$', views.deduction, name='deduction'),

                       # incentivenames crud
                       url(r'^incentives/$', views.incentivename_curd, name='incentivename_curd'),

                       # taxation crud
                       # url(r'^tax/scheme/$', views.tax_scheme, name='tax_scheme'),

                       # tax_detail_scheme crud
                       url(r'^taxschemedetail/add/$', views.tax_scheme_detail, name='add_tax_scheme'),
                       url(r'^taxschemedetail/edit/(?P<pk>[0-9]+)/$', views.tax_scheme_detail, name='edit_tax_scheme'),
                       # url(r'^taxschemedetail/delete/(?P<pk>[0-9]+)/$', views.delete_tax_scheme, name='delete_tax_scheme'),
                       url(r'^taxscheme/list/$', views.list_tax_scheme, name='list_tax_scheme'),

                        # tax_scheme crud
                       url(r'^taxscheme/add/$', views.tax_scheme, name='add_taxscheme'),
                       url(r'^taxscheme/edit/(?P<pk>[0-9]+)/$', views.tax_scheme, name='edit_taxscheme'),
                       url(r'^taxscheme/delete/(?P<pk>[0-9]+)/$', views.delete_taxscheme, name='delete_taxscheme'),
                       # url(r'^taxscheme/list/$', views.list_tax_scheme, name='list_tax_scheme'),
                       # url(r'^allowance/edit/(?P<pk>[0-9]+)/$', views.allowance, name='edit_allowance'),
                       # url(r'^by_branch/$', views.group_payroll_branch, name='group_payroll_branch'),
                       )
