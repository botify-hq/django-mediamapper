import urllib
import elementtree.ElementTree as ET
from django.utils.encoding import smart_str
from services.lastfm import BaseApi


class Api(BaseApi):
    NB_RESULTS_PER_PAGE = 50

    def _search_from_url(self, url, user):
        content = urllib.urlopen(url)
        dom = ET.parse(content)

        data = {'results': []}

        data['index'] = {
            'items_per_page': self.NB_RESULTS_PER_PAGE
        }

        entries = dom.getroot()
        for e in entries:
            nb_results = e.get('total')
            data['index'].update({
                'total_results': nb_results
            })

        images = entries.findall("images")


        for image in images:

            i = image.getchildren()

            for elem in i:
                tmp = elem.findtext("url")
                tmpsplit = tmp.split("images/")
                id = tmpsplit[1]

                owner_name = elem.findtext("owner/name")
                owner_url = elem.findtext("owner/url")
                

                current_result = {
                    'id': id,
                    'name': elem.findtext("title"),
                    'description': '',
                    'permalink_url': elem.findtext("url"),
                    'user_name': owner_name,
                    'user_url': owner_url
                }

                thumbs = elem.findall("sizes/size")
                for thumb in thumbs:
                    if thumb.get('name') == 'original':
                        image_url = thumb.text
                        current_result.update({
                            'image_url': image_url
                        })
                    if thumb.get('name') == 'large':
                        image_url_tn = thumb.text
                        current_result.update({
                            'image_url_tn': image_url_tn
                        })
                data['results'].append(current_result)

        return data


    def search_by_username(self, user, page):
        url = 'http://ws.audioscrobbler.com/2.0/?method=artist.getimages&artist=%s&api_key=%s&page=%d' % (
            smart_str(user), self.get_lastfm_api_key(), page)
        return self._search_from_url(url, user)