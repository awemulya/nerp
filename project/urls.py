from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
                       url(r'^imprest_ledger/$', views.ImprestLedger.as_view(), name='imprest_ledger'),
                       url(r'^imprest_ledger/save/$', views.save_imprest_ledger, name='save_imprest_ledger'),
                       url(r'^application/$', views.Application.as_view(), name='application'),
                       url(r'^application/save/$', views.save_application, name='save_application'),

                       url(r'^aids/$', views.AidList.as_view(), name='aid_list'),
                       url(r'^aid/add/$', views.AidCreate.as_view(), name='aid_add'),
                       url(r'^aid/edit/(?P<pk>\d+)/$', views.AidUpdate.as_view(),
                           name='aid_edit'),
                       url(r'^aid/delete/(?P<pk>\d+)/$', views.AidDelete.as_view(),
                           name='aid_delete'),
                       url(r'^projects/$', views.ProjectList.as_view(), name='project_list'),
                       url(r'^project/add/$', views.ProjectCreate.as_view(), name='project_add'),
                       url(r'^project/edit/(?P<pk>\d+)/$', views.ProjectUpdate.as_view(),
                           name='project_edit'),
                       url(r'^project/delete/(?P<pk>\d+)/$', views.ProjectDelete.as_view(),
                           name='project_delete'),

                       )
