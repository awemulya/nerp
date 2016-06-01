from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^login/$', views.web_login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    # url(r'^register/$', RegistrationView.as_view(form_class=UserRegistrationForm,
    #                                              template_name='registration/registration_form.html')),
    # url(r'^list$', UserList.as_view(), name='user-list'),
    # # url(r'^$', 'users.views.profile'),
    # url(r'^edit/$', 'users.views.edit_profile'),
    # url(r'^auth-error/$', 'users.views.auth_error'),
    # (r'^', include('registration.backends.default.urls')),
    # url(r'^(?P<username>[a-zA-Z0-9_.-]+)/$', 'users.views.profile', name='user-detail'),
]
