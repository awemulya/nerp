# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

from users import views as users_views

admin.autodiscover()


urlpatterns = [
    # Examples:
    url(r'^$', users_views.index, name='home'),
    url(r'^user/', include('users.urls')),
    # url(r'^app/', include('app.foo.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^inventory/', include('inventory.urls')),
    url(r'^library/', include('ils.urls')),
    url(r'^training/', include('training.urls')),
    url(r'^project/', include('project.urls')),
    url(r'^key/', include('key.urls')),
    # (r'^admin/settings/', include('dbsettings.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^froala_editor/', include('froala_editor.urls')),
    url(r'', include('core.urls')),
    url(r'^payroll/', include('hr.urls')),
]

if settings.DEBUG:
    urlpatterns += [] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
