# -*- coding: utf-8 -*-
from mapper.services.flickr.flickr import photos_search, photos_search_pages

from django.utils.encoding import smart_str

class Api(object):
    NB_RESULTS_PER_PAGE = 5

    def search_by_keyword(self, keyword, page=1):
        results = photos_search(text=smart_str(keyword), page=page, per_page=self.NB_RESULTS_PER_PAGE)

        data = {
            "index": {
                'total_results': 100,
                'items_per_page': self.NB_RESULTS_PER_PAGE
            },
            "results": []
        }

        for result in results:
            data['results'].append({
                'id': result.id,
                'name': result.title,
                'image_url': result.getLarge(),
                'image_url_tn': result.getThumbnail(),
                'description': result.description,
                'permalink_url': result.url,
                'user_name': result.owner.username,
                'user_url': 'http://www.flickr.com/people/%s/' % result.owner.username
            })

        return data


    def search_by_username(self, username, page=1):
        pass
