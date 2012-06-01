# -*- coding: utf-8 -*-
import urllib
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from types import NoneType

from django.utils.encoding import smart_str

class Api(object):
    NB_RESULTS_PER_PAGE = 30

    def _search_from_url(self, url):
        content = urllib.urlopen(url)
        dom = ET.parse(content)

        data = {'results': []}

        ns = '{http://www.w3.org/2005/Atom}'
        media_namespace = 'http://search.yahoo.com/mrss'
        itunes_namespace = 'http://www.itunes.com/dtds/podcast-1.0.dtd'
        dm_namespace = 'http://www.dailymotion.com/dmrss'


        #ET.tostring(dom.getroot())

        entries = dom.getroot().findall('channel/item')

        data['index'] = {
            'total_results': len(entries),
            'items_per_page': self.NB_RESULTS_PER_PAGE
        }

        for entry in entries:
            current_result = {
                'id': entry.findtext('{%s}id' % dm_namespace),
                'name': entry.findtext('title'),
                'image_url': entry.find('{%s}thumbnail' % media_namespace).get('url'),
                'description': entry.findtext('{%s}summary' % itunes_namespace),
                'embed_url': '',
                'embed_type': '',
                'duration': '',
                'permalink_url': entry.findtext('link'),
                'user_name': entry.findtext('{%s}author' % dm_namespace),
                'user_url': 'http://www.dailymotion.com/' + entry.findtext('{%s}author' % dm_namespace)
            }

            embed = entry.findall('{%s}group/{%s}content' % (media_namespace, media_namespace))
            for e in embed:
                current_result.update({
                    'embed_type' : e.get('type'),
                    'embed_url' : e.get('url'),
                    'duration': e.get('duration')
                })

            data['results'].append(current_result)
        return data



    def search_by_keyword(self, keyword, page=1):
        url = 'http://www.dailymotion.com/rss/relevance/search/%s/1' % smart_str(keyword)
        return self._search_from_url(url)

    def search_by_username(self, user, page=1):
        url = 'http://www.dailymotion.com/rss/user/%s/' % smart_str(user)
        return self._search_from_url(url)

    def search_by_location(self, lat, lng, page=1):
        pass
