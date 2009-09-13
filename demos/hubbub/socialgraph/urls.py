from django.conf.urls.defaults import *
 
urlpatterns = patterns('socialgraph.views',
    url(r'^follow/(?P<username>[a-zA-Z0-9_-]+)/$', 'follow', name='sg_follow'),
    url(r'^unfollow/(?P<username>[a-zA-Z0-9_-]+)/$', 'unfollow', name='sg_unfollow'),
    url(r'^search/$', 'search', name='sg_search'),
)