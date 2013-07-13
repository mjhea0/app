from django.conf.urls import patterns, include, url
from tastypie.api import Api
#from splintera.api.resources import MyModelResource

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#v1_api = Api(api_name='v1')
#v1_api.register(MyModelResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'splintera.views.home', name='home'),
    # url(r'^splintera/', include('splintera.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('splintera.registration.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^$', 'splintera.views.dashboard'),
    url(r'^code/(\d+)', 'splintera.views.code'),
#   url(r'^api/', include(v1_api.urls)),
)