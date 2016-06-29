from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.AccountList.as_view(), name='list_account'),
    url(r'^(?P<pk>[0-9]+)/$', views.ViewAccount.as_view(), name='view_ledger'),

    url(r'^parties/$', views.list_parties, name='list_parties'),
    url(r'^party/create/$', views.party_form, name='create_party'),
    url(r'^party/(?P<id>[0-9]+)/delete/$', views.delete_party, name='delete_party'),
    url(r'^party/(?P<id>[0-9]+)/$', views.party_form, name='update_party'),
    url(r'^parties.json$', views.parties_as_json, name='parties_as_json'),

    url(r'^categories/$', views.CategoryList.as_view(), name='category_list'),
    url(r'^category/add/$', views.CategoryCreate.as_view(), name='category_add'),
    url(r'^category/edit/(?P<pk>\d+)/$', views.CategoryUpdate.as_view(), name='category_edit'),
    url(r'^category/delete/(?P<pk>\d+)/$', views.CategoryDelete.as_view(), name='category_delete'),

    url(r'^account/$', views.AccountList.as_view(), name='account_list'),
    url(r'^account/add/$', views.AccountCreate.as_view(), name='account_add'),
    url(r'^account/edit/(?P<pk>\d+)/$', views.AccountUpdate.as_view(), name='account_edit'),
    url(r'^account/delete/(?P<pk>\d+)/$', views.AccountDelete.as_view(), name='account_delete'),

    # url(r'^receipts/$', views.list_receipts, name='list_receipts'),
    url(r'^receipt/create/$', views.receipt, name='create_receipt'),
    url(r'^receipt/(?P<pk>[0-9]+)/$', views.receipt, name='update_receipt'),
    # url(r'^receipt/(?P<id>[0-9]+)/delete/$', views.delete_receipt, name='delete_receipt'),
    url(r'^receipt/save/$', views.save_receipt, name='save_receipt'),

]
