from vimeo import VimeoClient
import urllib
import elementtree.ElementTree as ET

from django.conf import settings


class Api(object):
    NB_RESULTS_PER_PAGE = 30


    def _search_from_url(self, url):
        content = urllib.urlopen(url)
        dom = ET.parse(content)

        data = {'results': []}

        videos = dom.getroot()

        data['index'] = {
            'total_results': len(videos),
            'items_per_page': self.NB_RESULTS_PER_PAGE
        }

        for video in videos:
            current_result = {
                'id': video.find('id').text,
                'name': video.find('title').text,
                'permalink_url': 'http://vimeo.com/%s' % video.find('id').text,
                'description': video.find('description').text,
                'embed_url': 'http://player.vimeo.com/video/%s' % video.find('id').text,
                'embed_type': '',
                'duration': video.find('duration').text,
                'user_name': video.find('user_name').text,
                'user_url': video.find('user_url').text,
                'image_url': video.find('thumbnail_medium').text
            }
            data['results'].append(current_result)
            #print data
        return data


    def search_by_keyword(self, query, page=1):
        client = VimeoClient(settings.VIMEO_CONSUMER_KEY,
                             settings.VIMEO_CONSUMER_SECRET)

        videos = client.vimeo_videos_search(query=query)

        data = {'results': []}

        data['index'] = {
            'total_results': len(videos),
            'items_per_page': self.NB_RESULTS_PER_PAGE
        }

        for video in videos.getchildren():
            current_result = {
                'id': video.get('id'),
                'name': video.get('title'),
                'permalink_url': 'http://vimeo.com/%s' % video.get('id'),
                'description': '',
                'embed_url': 'http://player.vimeo.com/video/%s' % video.get('id'),
                'embed_type': '',
                'duration': '',
                'user_name': '',
                'user_url': ''
            }
            response = client.vimeo_videos_getThumbnailUrls(video_id=video.get('id'))
            thumbnails = response.getchildren()
            information = client.vimeo_videos_getInfo(video_id=video.get('id'))

            if len(information):
                current_result.update({
                    'description': information.find('description').text,
                    'duration': information.find('duration').text,
                    'user_name': information.find('owner').get('display_name'),
                    'user_url': information.find('owner').get('profileurl')
                })

            if len(thumbnails) > 1:
                current_result['image_url'] = thumbnails[1].text

            data['results'].append(current_result)
        return data

    def search_by_username(self, user, page=1):
        url = 'http://vimeo.com/api/v2/%s/all_videos.xml' % user
        return self._search_from_url(url)

    def search_by_location(self, lat, lng, page=1):
        pass