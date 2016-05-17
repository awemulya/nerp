from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',

                       url(r'^parties/$', views.list_parties, name='list_parties'),
                       url(r'^party/create/$', views.party_form, name='create_party'),
                       url(r'^party/(?P<id>[0-9]+)/delete/$', views.delete_party, name='delete_party'),
                       url(r'^party/(?P<id>[0-9]+)/$', views.party_form, name='update_party'),
                       url(r'^parties.json$', views.parties_as_json, name='parties_as_json'),

                       url(r'^employees/$', views.list_employees, name='list_employees'),
                       url(r'^employee/create/$', views.employee_form, name='create_employee'),
                       url(r'^employee/(?P<id>[0-9]+)/delete/$', views.delete_employee, name='delete_employee'),
                       url(r'^employee/(?P<id>[0-9]+)/$', views.employee_form, name='update_employee'),
                       url(r'^employees.json$', views.employees_as_json, name='employees_as_json'),

                       url(r'^budget_heads.json$', views.budget_heads_as_json, name='budget_heads_as_json'),
                       url(r'^accounts.json$', views.accounts_as_json, name='accounts_as_json'),
                       url(r'^activities.json$', views.activities_as_json, name='activities_as_json'),
                       url(r'^donors.json$', views.donors_as_json, name='donors_as_json'),
                       url(r'^tax_schemes.json$', views.tax_schemes_as_json, name='tax_schemes_as_json'),
                       url(r'^languages.json$', views.languages_as_json, name='languages_as_json'),

                       url(r'^change_calendar/$', views.change_calendar, name='change_calendar'),

                       url(r'^admin/change_fiscal_year/$', views.change_fiscal_year, name='change_fiscal_year'),

                       url(r'^donors/$', views.DonorList.as_view(), name='donor_list'),
                       url(r'^donor/add/$', views.DonorCreate.as_view(), name='donor_add'),
                       url(r'^donor/edit/(?P<pk>\d+)/$', views.DonorUpdate.as_view(), name='donor_edit'),
                       url(r'^donor/delete/(?P<pk>\d+)/$', views.DonorDelete.as_view(), name='donor_delete'),

                       )