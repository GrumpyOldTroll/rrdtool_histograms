from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

import sys

urlpatterns = patterns('',
    # Example:
    #  old version: (r'^rrd/(?P<start>\d+)/(?P<length>\d+)/?', 'mysite.rrd.views.index'),
    (r'^rrd(?:/?(?:\?.*)?)?$', 'mysite.rrd.views.index'),
    # (r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
if len(sys.argv) > 1:
    if sys.argv[0]=='manage.py' and sys.argv[1] == 'runserver':
        urlpatterns.extend(patterns('', (r'^rrd/static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/cygdrive/c/Documents and Settings/Educator/Desktop/Jonathan/mysite'}),))
        # print 'extended urlpatterns to %s' % (str(urlpatterns))
    

