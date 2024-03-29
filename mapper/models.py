# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from extended_choices import Choices

EMBED_FLASH_CODE = """
<object width="%(width)d" height="%(height)d">\
<param name="movie" value="%(url)s"></param>\
<param name="allowFullScreen" value="true"></param>\
<param name="allowscriptaccess" value="always"></param>\
<embed src="%(url)s" type="application/x-shockwave-flash" width="%(width)d" height="%(height)d" allowscriptaccess="always" allowfullscreen="true"></embed>\
</object>
"""

EMBED_IFRAME = '<iframe src="%(url)s" width="%(width)d" height="%(height)d">'\
               '</iframe>'
EMBED_IMG = '<img src="%(url)s" width="%(width)d" height="%(height)d">'

class MapperBaseModel(models.Model):
    class Meta:
        abstract = True
	app_label = 'mapper'


class Media(MapperBaseModel):
    TYPE_CHOICES = Choices(('PHOTO',1, 'Photo'),('VIDEO',2, 'Video'))

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    type = models.PositiveIntegerField(choices=TYPE_CHOICES.CHOICES)
    image_url = models.CharField(max_length=250, blank=True, null=True)
    image_url_tn = models.CharField(max_length=250, blank=True, null=True)
    service = models.CharField(max_length=250)
    service_object_id = models.CharField(max_length=250)
    permalink_url = models.CharField(max_length=250, blank=True, null=True)
    user_name = models.CharField(max_length=250, blank=True, null=True)
    user_url = models.CharField(max_length=250, blank=True, null=True)

    class Meta(MapperBaseModel.Meta):
        pass

    def __unicode__(self):
        return self.name


class MediaVideo(Media):
    duration = models.PositiveIntegerField(default=0)
    embed_url = models.CharField(max_length=250, blank=True, null=True)
    embed_type = models.CharField(max_length=250, blank=True, null=True)

    def get_embed(self, width=450, height=300):
        if self.embed_type == "application/x-shockwave-flash":
            return EMBED_FLASH_CODE % {'width': width, 'height': height, 'url': self.embed_url}
        return EMBED_IFRAME % {'width': width, 'height': height, 'url': self.embed_url}

    def save(self, *args, **kwargs):
        self.type = Media.TYPE_CHOICES.VIDEO
        return super(MediaVideo, self).save(*args, **kwargs)

class MediaPhoto(Media):

    def save(self, *args, **kwargs):
        self.type = Media.TYPE_CHOICES.PHOTO
        return super(MediaPhoto, self).save(*args, **kwargs)


class Keyword(MapperBaseModel):
    keyword = models.CharField(max_length=250)

    def __unicode__(self):
        return self.keyword


class EntryKeyword(MapperBaseModel):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    keyword = models.ForeignKey(Keyword)
    date_creation = models.DateTimeField(auto_now_add=True)


class MediaKeyword(MapperBaseModel):
    media = models.ForeignKey(Media)
    keyword = models.ForeignKey(Keyword)
    date_creation = models.DateTimeField(auto_now_add=True)


class MediaType(MapperBaseModel):
    name = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name


class MediaEntryManager(models.Manager):
    def filter_object(self, object):
        content_type = ContentType.objects.get_for_model(object)
        return self.filter(content_type = content_type, object_id = object.id) 

class MediaEntryQueryset(QuerySet):
    def filter_object(self, object):
        return self.get_queryset().object(object)

class MediaEntry(MapperBaseModel):
    media = models.ForeignKey('Media')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    position = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User)
    date_creation = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    media_type = models.ForeignKey(MediaType, blank=True, null=True)

    objects = MediaEntryManager()

    def __unicode__(self):
        return u"%s on %s" % (self.media, self.content_object)

    def __init__(self, *args, **kwargs):
        super(MapperBaseModel, self).__init__(*args, **kwargs)
	attr_list = ('image_url', 'image_url_tn', 'service', 'permalink_url', 'user_name', 'user_url')
        for attr in attr_list:
            setattr(self, attr, getattr(self.media, attr))
        if self.media.type == Media.TYPE_CHOICES.VIDEO:
            v = MediaVideo.objects.get(pk=self.media.id)
            for attr in ('duration', 'embed_url', 'embed_type'):
                setattr(self, attr, getattr(v, attr))
        
    class Meta(MapperBaseModel.Meta):
        verbose_name_plural = 'Media Entries' 

    def get_embed(self, width=450, height=300):
        if self.media.type == Media.TYPE_CHOICES.VIDEO:
            if self.embed_type == "application/x-shockwave-flash":
                return EMBED_FLASH_CODE % {'width': width, 'height': height, 'url': self.embed_url}
            return EMBED_IFRAME % {'width': width, 'height': height, 'url': self.embed_url}
        else:
            return EMBED_IMG % {'width': width, 'height': height, 'url': self.embed_url}

    def name_is_custom(self):
        return self.name and self.name != self.media.name

    def description_is_custom(self):
        return self.description and self.description != self.media.description

    @property
    def final_name(self):
        if self.name:
            return self.name
        return self.media.name

    @property
    def final_description(self):
        if self.description:
            return self.description
        return self.media.description

