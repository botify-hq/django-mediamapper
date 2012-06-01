import cgi
import urllib

from django.conf import settings

class BaseApi(object):

    ACCESS_TOKEN_URL = 'https://graph.facebook.com/oauth/access_token'

    def get_access_token(self, **kwargs):
        if not 'client_id' in kwargs:
            kwargs['client_id'] = self.get_facebook_app_id()

        if not 'client_secret' in kwargs:
            kwargs["client_secret"] = self.get_facebook_api_secret()

        if not 'grant_type' in kwargs:
            kwargs['grant_type'] = 'client_credentials'

        response = cgi.parse_qs(urllib.urlopen(
            "%s?" % self.get_access_token_url()
            + urllib.urlencode(kwargs)).read()
        )

        access_token = response["access_token"][-1]

        return access_token

    def get_access_token_url(self):
        return self.ACCESS_TOKEN_URL

    def get_facebook_app_id(self):
        return settings.MEDIA_MAPPER_KEYS['FACEBOOK_APP_ID']

    def get_facebook_api_secret(self):
        return settings.MEDIA_MAPPER_KEYS['FACEBOOK_APP_SECRET']
        
