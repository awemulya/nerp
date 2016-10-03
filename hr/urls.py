from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter

import views
from hr import api

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'grade-scale', api.EmployeeGradeScaleViewSet)
router.register(r'grade-group', api.EmployeeGradeGroupViewSet)
router.register(r'grade-scale-validity', api.GradeScaleValidityViewSet)
router.register(r'employee-grade', api.EmployeeGradeViewSet)

urlpatterns = patterns('',
                       url(r'^api/', include(router.urls)),
                       # url(r'^api/', include('rest_framework.urls', namespace='hr-api')),
                       url(r'^$', views.payroll_index, name='payroll_index'),
                       url(r'^entry/$', views.payroll_entry, name='payroll_entry'),
                       url(r'^(?P<pk>[0-9]+)/$', views.payroll_entry, name='payroll_entry'),
                       url(r'^get_employee_account/$', views.get_employee_account, name='get_employee_account'),
                       url(r'^get_employees_account/$', views.get_employees_account, name='get_employees_account'),
                       url(r'^save_payroll_entry/$', views.save_payroll_entry, name='save_payroll_entry'),
                       url(r'^save_payroll_entry/(?P<pk>[0-9]+)/$', views.save_payroll_entry,
                           name='save_payroll_entry_edit'),
                       url(r'^entry_detail/(?P<pk>[0-9]+)/$', views.entry_detail, name='entry_detail'),
                       url(r'^entry_list/$', views.entry_list, name='entry_list'),
                       url(r'^get_employee_options/$', views.get_employee_options, name='get_employee_options'),
                       url(r'^approve_entry/(?P<pk>[0-9]+)/$', views.approve_entry, name='approve_entry'),
                       url(r'^transact_entry/(?P<pk>[0-9]+)/$', views.transact_entry, name='transact_entry'),
                       url(r'^delete_entry/(?P<pk>[0-9]+)/$', views.delete_entry, name='delete_entry'),

                       # employee crud
                       url(r'^employee/add/$', views.employee, name='add_employee'),
                       url(r'^employee/edit/(?P<pk>[0-9]+)/$', views.employee, name='edit_employee'),
                       url(r'^employee/toggle_activeness/(?P<pk>[0-9]+)/$', views.toggle_employee_activeness,
                           name='toggle_employee_activeness'),
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

                       # Employee Grade
                       url(r'^employee-grade-group/$', views.employee_grade_group, name='employee_grade_group'),
                       url(r'^employee-grade/$', views.employee_grade, name='employee_grade'),

                       # Employee Designation
                       url(r'^designations/$', views.employee_designation, name='employee_designation'),

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
                       url(r'^report/$', views.get_report, name='get_report'),
                       # url(r'^generate_report/$', views.generate_report, name='generate_report'),

                       # report setting crud
                       url(r'^report-setting/add/$', views.report_setting, name='add_report_setting'),
                       url(r'^report-setting/edit/(?P<pk>[0-9]+)/$', views.report_setting, name='edit_report_setting'),
                       url(r'^report-setting/delete/(?P<pk>[0-9]+)/$', views.delete_report_setting,
                           name='delete_report_setting'),
                       url(r'^report-seting/list/$', views.list_report_setting, name='list_report_setting'),

                       # GradeScale
                       url(r'^grades-scale-entry/$', views.grades_scale, name='grade-scale-entry'),
                       # EndGradeScale

                       )
