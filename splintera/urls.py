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
    url(r'^repos', 'splintera.views.repos'),
    url(r'^clone_repo', 'splintera.views.clone_repo'),
    url(r'^commit_test_to_repo', 'splintera.views.commit_test_to_repo'),
    url(r'^code_tree', 'splintera.views.code_tree'),
    url(r'^store_test_in_folder', 'splintera.views.store_test_in_folder'),
#   url(r'^api/', include(v1_api.urls)),
)