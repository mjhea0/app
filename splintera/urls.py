from django.conf.urls import patterns, include, url
from tastypie.api import Api
#from flow.api.resources import MyModelResource

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#v1_api = Api(api_name='v1')
#v1_api.register(MyModelResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'flow.views.home', name='home'),
    # url(r'^flow/', include('flow.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('flow.registration.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^$', 'flow.views.homepage'),
    url(r'^api/', 'flow.views.api'),
    url(r'^one/', 'flow.views.one'),
    url(r'^two/', 'flow.views.two'),
    url(r'^three/', 'flow.views.three'),
    url(r'^four/', 'flow.views.four'),
#   url(r'^api/', include(v1_api.urls)),
)