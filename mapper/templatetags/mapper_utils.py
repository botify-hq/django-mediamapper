# -*- coding: utf-8 -*-
from django import template
from django.contrib.contenttypes.models import ContentType

from mapper.models import MediaEntry, Media

register = template.Library()

@register.filter
def media_is_recorded(media, entry):
    # TODO A mettre sous redis pour plus de rapidité
    try:
        if isinstance(media, dict):
            media_id = media['id']
        elif isinstance(media, Media):
            media_id = media.id
        
        me = MediaEntry.objects.get(object_id=entry.id, content_type=ContentType.objects.get_for_model(entry), media__id=media_id)
    except MediaEntry.DoesNotExist:
        return False
    else:
        return me.active
