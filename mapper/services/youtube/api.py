# -*- coding: utf-8 -*-
import urllib
from types import NoneType

from django.utils.encoding import smart_str

from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET

class Api(object):
    NB_RESULTS_PER_PAGE = 30

    def _search_from_url(self, url):
        content = urllib.urlopen(url)
        dom = ET.parse(content)

        data = {'results': []}

        ns = '{http://www.w3.org/2005/Atom}'
        ns_yt = '{http://gdata.youtube.com/schemas/2007}'
        ns_media = '{http://search.yahoo.com/mrss/}'
        ns_os = '{http://a9.com/-/spec/opensearchrss/1.0/}'

        #ET.tostring(dom.getroot())

        data['index'] = {
            'total_results': int(dom.getroot().find(ns_os + 'totalResults').text),
            'items_per_page': self.NB_RESULTS_PER_PAGE
        }

        entries = dom.getroot().findall(ns + 'entry')


        #print to
        for entry in entries:
            state = entry.find(ns_yt + 'state')
            if state and state['name'] != "restricted":
                continue
            else:
                media_group = entry.find(ns_media + 'group')
                media_content = media_group.find(ns_media + 'content')

                if type(media_content) == NoneType:
                    continue

                data['results'].append({
                    'id': entry.find(ns + 'id').text.replace('http://gdata.youtube.com/feeds/api/videos/', ''),
                    'name': entry.find(ns + 'title').text,
                    'image_url': media_group.find(ns_media + 'thumbnail').get('url'),
                    'description': entry.find(ns + 'content').text,
                    'permalink_url': media_group.find(ns_media + 'player').get('url'),
                    'embed_url': media_content.get('url'),
                    'embed_type': media_content.get('type'),
                    'duration': media_content.get('duration'),
                    'user_name': entry.find(ns + 'author').find(ns + 'name').text,
                    'user_url': entry.find(ns + 'author').find(ns + 'uri').text.replace('gdata', 'www').replace(
                        'feeds/api/users', 'user')
                })
        return data

    def search_by_keyword(self, keyword, page=1):
        url = 'http://gdata.youtube.com/feeds/api/videos?q=%s&racy=include&orderby=relevance&v=1&max-results=%d&start-index=%d' % (
            smart_str(keyword), self.NB_RESULTS_PER_PAGE, (page - 1) * self.NB_RESULTS_PER_PAGE + 1)
        return self._search_from_url(url)

    def search_by_username(self, user, page=1):
        url = 'http://gdata.youtube.com/feeds/api/users/%s/uploads' % smart_str(user)
        return self._search_from_url(url)

    def search_by_location(self, lat, lng, page=1):
        pass
