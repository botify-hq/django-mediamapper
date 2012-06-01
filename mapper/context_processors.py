# -*- coding: utf-8 -*-
from mapper.utils import get_content_types
from mapper.service import Service, get_services, get_photos_services, get_videos_services

def services(request):
    return {
	'content_types': get_content_types(),
        'services': get_services(),
        'services_photos': get_photos_services(),
        'services_videos': get_videos_services(),
    }
