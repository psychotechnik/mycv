from django.conf import settings
from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()

handler500 = 'mycv.apps.core.views.server_error'

urlpatterns = patterns(
    'mycv.apps.core.views', url(r'^$', TemplateView.as_view(template_name='about.html'), name='about'),
)
urlpatterns += patterns(
    'mycv.apps.projects.views',
    url(r'^resume/$', 'client_list_view', name='client_list'),
)

urlpatterns += patterns(
    'mycv.apps.projects.views',
    url(r'^projects/', include('mycv.apps.projects.urls', namespace='projects', app_name='projects')),
)

    #url(r'^404/$', TemplateView.as_view(template_name='404.html'), name='404'),
    #url(r'^500/$', TemplateView.as_view(template_name='500.html'), name='500'),
    #url(r'^502/$', TemplateView.as_view(template_name='502.html'), name='502'),
    #url(r'^humans.txt$', TemplateView.as_view(template_name='humans.txt'), name='humans'),
    #url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt'), name='robots'),

if 'grappelli' in settings.INSTALLED_APPS:
    urlpatterns += patterns(
        '',
        url(r'^grappelli/', include('grappelli.urls')),
    )

urlpatterns += patterns(
    '',
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns += patterns(
            '',
            url(r'^__debug__/', include(debug_toolbar.urls)),
        )
