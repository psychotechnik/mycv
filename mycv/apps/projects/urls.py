try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

# place app url patterns here

urlpatterns = patterns('mycv.apps.projects.views',
    url(r'^all/$', 'project_list_view', name='project_list'),
)
