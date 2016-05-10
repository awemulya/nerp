from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
                       url(r'^imprest_ledger/$', views.ImprestLedger.as_view(), name='imprest_ledger'),
                       url(r'^imprest_ledger/save/$', views.save_imprest_ledger, name='save_imprest_ledger'),
                       url(r'^application/$', views.Application.as_view(), name='application'),
                       # url(r'^imprest_ledger/save/$', views.save_imprest_ledger, name='save_imprest_ledger'),
                       )
