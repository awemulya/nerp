from django.conf.urls import url
import views

urlpatterns = [

    url(r'^request/$', views.send_key_request, name='send_key_request'),
    url(r'^activation/$', views.activation, name='key_activation'),
    # url(r'^invalid/$', views.invalid_key, name='invalid_key'),

]
