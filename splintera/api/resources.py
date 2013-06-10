from tastypie.resources import MessageResource
from tastypie.resources import ModelResource
#from flow.models import RegistrationProfile

# for SQL backends, use ModelResource
"""class MyModelResource(ModelResource):
    class Meta:
        queryset = RegistrationProfile.objects.all()
        allowed_methods = ['get']"""

# for our non-SQL backend, we'll use a custom handler to implement the 9 required methods
# we'll just do the GET requests for now
'''
detail_uri_kwargs
get_object_list
obj_get_list
obj_get
obj_create
obj_update
obj_delete_list
obj_delete
rollback
'''

'''class MessageResource(Resource):
    # Just like a Django ``Form`` or ``Model``, we're defining all the
    # fields we're going to handle with the API here.
    uuid = fields.CharField(attribute='uuid')
    user_uuid = fields.CharField(attribute='user_uuid')
    message = fields.CharField(attribute='message')
    created = fields.IntegerField(attribute='created')

    class Meta:
        resource_name = 'openTSDB'
        object_class = RiakObject
        authorization = Authorization()

    def _bucket(self):
        client = self._client()
        # Note that we're hard-coding the bucket to use. Fine for
        # example purposes, but you'll want to abstract this.
        return client.bucket('messages')

    # The following methods will need overriding regardless of your
    # data source.
    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.uuid
        else:
            kwargs['pk'] = bundle_or_obj.uuid

        return kwargs

    def get_object_list(self, request):
        raise NotImplementedError

    def obj_get_list(self, request=None, **kwargs):
        # Filtering disabled for brevity...
        raise NotImplementedError

    def obj_get(self, request=None, **kwargs):
        bucket = self._bucket()
        message = bucket.get(kwargs['pk'])
        return RiakObject(initial=message.get_data())

    def obj_create(self, bundle, request=None, **kwargs):
        raise NotImplementedError

    def obj_update(self, bundle, request=None, **kwargs):
        raise NotImplementedError

    def obj_delete_list(self, request=None, **kwargs):
        raise NotImplementedError

    def obj_delete(self, request=None, **kwargs):
        raise NotImplementedError

    def rollback(self, bundles):
        pass'''