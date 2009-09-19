import os

from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'hubbub.views.index', name='index'),
    (r'^friends/', include('socialgraph.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    from django.contrib import admin
    ADMIN_PATH = os.path.join(os.path.dirname(admin.__file__), 'media')
    urlpatterns += patterns('',
        (r'^media/admin/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': ADMIN_PATH, 'show_indexes': True}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
