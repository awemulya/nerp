from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^$', views.payroll_entry, name='payroll_entry'),
                       # url(r'^by_branch/$', views.group_payroll_branch, name='group_payroll_branch'),
                       )
