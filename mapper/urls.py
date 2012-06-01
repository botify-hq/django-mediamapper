from django.conf.urls.defaults import *

from mapper.views import *

urlpatterns = patterns(
    'mapper.views',
    url(r'^$',
        home,
        name='home'),

    url(r'^(?P<model_id>\d+)/$',
        model_home,
        name='model_home'),
                       
    url(r'^search$',
        model_search,
        name='model_search'),

    url(r'^(?P<model_id>\d+)/entry/(?P<entry_id>\d+)/$',
        entry,
        name='entry'),

    url(r'^(?P<model_id>\d+)/entry/(?P<entry_id>\d+)/sort/$',
        entry_sort,
        name='entry_sort'),

    url(r'^(?P<model_id>\d+)/entry/(?P<entry_id>\d+)/search/$',
        entry_service_search,
        name='entry_search'),

    url(r'^(?P<model_id>\d+)/entry/(?P<entry_id>\d+)/service/(?P<service_slug>[\w.:@+-]+)/object/(?P<object_id>\d+)/preview/$',
        entry_preview,
        name='entry_preview'),

    url(r'^(?P<model_id>\d+)/entry/(?P<entry_id>\d+)/service/(?P<service_slug>[\w.:@+-]+)/object/(?P<object_id>\d+)/search_from_url/$',
        entry_from_album_service_search,
        name='entry_from_album_search'),

    url(r'^(?P<model_id>\d+)/entry/(?P<entry_id>\d+)/media/(?P<media_id>\d+)/add/$',
        add_media,
        name='entry_add_media'),

    url(r'^(?P<model_id>\d+)/entry/(?P<entry_id>\d+)/media/(?P<media_id>\d+)/remove/$',
        remove_media,
        name='entry_remove_media'),
                       
    url(r'^(?P<model_id>\d+)/entry/(?P<entry_id>\d+)/media/(?P<media_id>\d+)/edit_field/$',
        edit_media_field,
        name='edit_media_field'),
                       
    url(r'^(?P<model_id>\d+)/entry/(?P<entry_id>\d+)/media/(?P<media_id>\d+)/rollback_field/$',
        rollback_media_field,
        name='rollback_media_field'),
                       
)
