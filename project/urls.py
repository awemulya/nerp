from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='project_index'),
                       url(r'^(?P<project_id>[0-9]+)/imprest_ledger/$', views.ImprestLedger.as_view(), name='imprest_ledger'),
                       url(r'^(?P<project_id>[0-9]+)/imprest_ledger/save/$', views.save_imprest_ledger, name='save_imprest_ledger'),
                       url(r'^(?P<project_id>[0-9]+)/application/$', views.Application.as_view(), name='application'),
                       url(r'^(?P<project_id>[0-9]+)/application/save/$', views.save_application, name='save_application'),
                       )
