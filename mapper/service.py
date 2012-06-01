import copy

from django.conf import settings
from django.utils.importlib import import_module
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from mapper.exceptions import ServiceApiException
from mapper.models import MediaPhoto, MediaVideo, Keyword, MediaKeyword, EntryKeyword

from extended_choices import Choices

class Service(object):
    PHOTO_KEYS = ('name', 'description', 'image_url', 'permalink_url', 'user_name', 'user_url',)
    VIDEO_KEYS = (
    'name', 'description', 'image_url', 'permalink_url', 'user_name', 'user_url', 'embed_url', 'embed_type', 'duration'
    ,)

    def __unicode__(self):
        return self.name

    def pprint(self):
        return self.__dict__

    def _get_media_class(self):
        if self.type == "PHOTO":
            return MediaPhoto
        return MediaVideo

    def __init__(self, *args, **kwargs):
        self.record_results = False

    def get_object(self, object_id):
        return self._get_media_class().objects.get(pk=object_id)

    def _check_data_validity(self, results):
        if not type(results) is dict:
            raise ServiceApiException("Result var must be a dict : %s" % str(results))
        if not results.has_key('index'):
            raise ServiceApiException("Key 'index' not found for Result : %s" % str(results))
        else:
            if not results['index'].has_key('total_results'):
                raise ServiceApiException("Key 'total_results' not found for Result : %s" % str(results))
            if not results['index'].has_key('items_per_page'):
                raise ServiceApiException("Key 'items_per_page' not found for Result : %s" % str(results))

        if not results.has_key('results'):
            raise ServiceApiException("Key 'results' not found for Result : %s" % str(results))
        else:
            if self.type == "VIDEO":
                keys = self.VIDEO_KEYS
            else:
                keys = self.PHOTO_KEYS

            for data in results['results']:
                for key in keys:
                    if not data.has_key(key):
                        raise ServiceApiException("Key '%s' not found for Result : %s" % (key, str(data),))

    def _map_video_data(self, data):
        final_data = copy.deepcopy(data)
        del final_data['id']
        return final_data

    def return_objects_from_results(self, entry, results, keyword=None):
        list = []
        for result in results:
            try:
                ct = ContentType.objects.get_for_model(entry)
                obj, created = self._get_media_class().objects.get_or_create(service=self.slug,
									     content_type = ct,
									     object_id = entry.id,
                                                                             service_object_id=result['id'])
                obj.__dict__.update(self._map_video_data(result))
                obj.save()
                list.append(obj)

                if keyword:
                    MediaKeyword.objects.get_or_create(media=obj, keyword=keyword)
            except ServiceApiException, e:
                return ('error', e.msg)
        return list

    def search_by_keyword(self, keyword, page=1, entry=None, return_objects=False, check_validity=True):
        if not self.implements_keywords_search:
            raise ServiceApiException("Search by Keyword is not enabled on Service %s" % self.name)
        if not hasattr(self.api, 'search_by_username'):
            raise ServiceApiException("Search by Keyword Method is not enabled on Service %s API" % self.name)

        keyword_obj, created = Keyword.objects.get_or_create(keyword=keyword)

        if entry:
            ct = ContentType.objects.get_for_model(entry)
            EntryKeyword.objects.get_or_create(content_type = ct, object_id=entry.id, keyword=keyword_obj)

        results = self.api.search_by_keyword(keyword, page)

        if check_validity:
            self._check_data_validity(results)

            # return objects only if check validy is enabled
            if return_objects:
                results['results'] = self.return_objects_from_results(entry, results['results'], keyword=keyword_obj)

        return results

    def search_by_username(self, username, page, entry=None, return_objects=False, check_validity=True):
        if not self.implements_user_search:
            raise ServiceApiException("Search by Username is not enabled on Service %s" % self.name)
        if not hasattr(self.api, 'search_by_username'):
            raise ServiceApiException("Search by Username Method is not enabled on Service %s API" % self.name)

        results = self.api.search_by_username(username, page)

        if check_validity:
            self._check_data_validity(results)

            # return objects only if check validy is enabled
            if return_objects:
                results['results'] = self.return_objects_from_results(entry, results['results'])
        return results

    def search_albums_by_username(self, username, page=1, entry=None, return_objects=False, check_validity=True):
        if not self.implements_user_search:
            raise ServiceApiException("Search by Username is not enabled on Service %s" % self.name)
        if not hasattr(self.api, 'search_by_username'):
            raise ServiceApiException("Search by Username Method is not enabled on Service %s API" % self.name)

        results = self.api.search_albums_by_username(username)

        # todo check validity for albums

        return results


    def search_by_album_id(self, album_id, page=1, entry=None, return_objects=False, check_validity=True):
        if not self.implements_user_search:
            raise ServiceApiException("Search by Username is not enabled on Service %s" % self.name)
        if not hasattr(self.api, 'search_by_username'):
            raise ServiceApiException("Search by Username Method is not enabled on Service %s API" % self.name)

        results = self.api.get_medias_from_album_id(album_id)

        # todo check validity for photos from albums

        results['results'] = self.return_objects_from_results(entry, results['results'])

        return results


def load_services():
    services = []
    for s in settings.MEDIA_MAPPER_SERVICES:
	config = import_module("%s.config" % s)
	service = Service()
	service.type = config.TYPE.upper()
	service.name = config.NAME
	service.slug = config.SLUG
	service.url = config.URL
	service.description = config.DESCRIPTION
	service.implements_keywords_search = config.IMPLEMENTS_KEYWORDS_SEARCH
	service.implements_user_search = config.IMPLEMENTS_USER_SEARCH
	service.implements_location_search = config.IMPLEMENTS_LOCATION_SEARCH
	service.implements_user_albums = config.IMPLEMENTS_USER_ALBUMS
        mod = import_module("%s.api" % s)
        service.api = getattr(mod, 'Api')()
        services.append(service)
    return services

services = load_services()

def get_services():
    return services

def get_photos_services():
    return [s for s in services if s.type == "PHOTO"]

def get_videos_services():
    return [s for s in services if s.type == "VIDEO"]

def get_service_from_slug(slug):
    for s in services:
        if s.slug == slug:
            return s
    return None
