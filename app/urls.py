from django.conf.urls import patterns, include, url
# from app.admin import admin_site
from django.conf import settings
from django.contrib import admin
from users import views as users_views

# admin.site = admin_site
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', users_views.index, name='home'),
                       (r'^user/', include('users.urls')),
                       # url(r'^app/', include('app.foo.urls')),

                       (r'^account/', include('account.urls')),
                       (r'^inventory/', include('inventory.urls')),
                       (r'^library/', include('ils.urls')),
                       (r'^training/', include('training.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       (r'^i18n/', include('django.conf.urls.i18n')),

                       url(r'^froala_editor/', include('froala_editor.urls')),

                       (r'^settings/', include('dbsettings.urls')),

                       (r'', include('core.urls')),


                       )

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$',
                                'django.views.static.serve',
                                {'document_root': settings.MEDIA_ROOT,
                                 }))
    urlpatterns += patterns('',
                            url(r'^static/(?P<path>.*)$',
                                'django.views.static.serve',
                                {'document_root': settings.STATIC_ROOT,
                                 }))
