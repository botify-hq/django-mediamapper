import urllib
from django.utils.encoding import smart_str

from facebook import GraphAPI
from mapper.services.facebook import BaseApi


class Api(BaseApi):
    NB_RESULTS_PER_PAGE = 30

    def search_by_username(self, user, page=1):
        data = {'results': []}

        access_token = self.get_access_token()

        api = GraphAPI(access_token)

        results = api.request('%s/photos' % smart_str(user), args={'fields':'id,picture,source,images, link, from'})
        result = results['data']

        data['index'] = {
            'total_results': len(result),
            'items_per_page': self.NB_RESULTS_PER_PAGE
        }

        for r in result:
            data['results'].append({
                'id': r['id'],
                'name': '',
                'image_url': r['source'],
                'image_url_tn': r['picture'],
                'description': '',
                'permalink_url': r['link'],
                'user_name': r['from']['name'],
                'user_url': 'http://www.facebook.com/%s' % smart_str(user)
            })
        return data

    
    def search_albums_by_username(self, user, page=1):
        data = {'results': []}

        access_token = self.get_access_token()

        api = GraphAPI(access_token)

        results = api.request('%s/albums' % smart_str(user), args={'fields':'id,name,link,from,cover_photo'})
        result = results['data']

        data['index'] = {
            'total_results': len(result),
            'items_per_page': self.NB_RESULTS_PER_PAGE
        }
        
        for r in result:
            file = urllib.urlopen("https://graph.facebook.com/%s/picture?" % r['id']
                                    + urllib.urlencode({'access_token': access_token}))
            image_url = file.url
            file.close()

            data['results'].append({
                'id': r['id'],
                'name': r['name'],
                'image_url': image_url,
                'image_url_tn': image_url,
                'description': '',
                'permalink_url': r['link'],
                'user_name': r['from']['name'],
                'user_url': r['from']['id']
            })
        return data

    
    def get_medias_from_album_id(self, album_id):
        data = {'results': []}

        access_token = self.get_access_token()

        api = GraphAPI(access_token)

        results = api.request('%s/photos' % smart_str(album_id), args={'fields':'id,name,picture,source,images,link,from'})
        result = results['data']

        data['index'] = {
            'total_results': len(result),
            'items_per_page': self.NB_RESULTS_PER_PAGE
        }

        for r in result:
            data['results'].append({
                'id': r['id'],
                'name': r['name'],
                'image_url': r['source'],
                'image_url_tn': r['picture'],
                'description': '',
                'permalink_url': r['link'],
                'user_name': r['from']['name'],
                'user_url': 'http://www.facebook.com/'+r['from']['id']
            })
        return data
