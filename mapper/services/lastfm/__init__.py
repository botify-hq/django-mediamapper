from django.conf import settings

class BaseApi(object):

    LASTFM_API_URL = 'http://ws.audioscrobbler.com/2.0/'

    def get_lastfm_api_url(self):
        return self.LASTFM_API_URL

    def get_lastfm_api_key(self):
        return settings.LASTFM_API_KEY
        