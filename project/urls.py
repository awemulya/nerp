from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
                       url(r'^imprest_ledger$', views.ImprestLedger.as_view(), name='imprest_ledger'),
                       # url(r'^receipt/(?P<pk>[0-9]+)/$', views.receipt, name='update_receipt'),
                       # url(r'^receipt/save/$', views.save_receipt, name='save_receipt'),

                       )
