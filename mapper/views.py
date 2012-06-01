# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date
import time
import json

from django.shortcuts import render_to_response, get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.sites.models import Site

from mapper.models import *
from mapper.service import get_service_from_slug
from mapper.utils import get_content_types, get_content_type

def home(request):
    if request.user.is_authenticated() and request.user.is_staff:
        return render(request, 'mapper/home.html')
    else:
        return HttpResponseRedirect(reverse('admin:login'))


@login_required
def model_home(request, model_id):
    ct = ContentType.objects.get(pk=model_id)
    
    if not request.user.is_staff:
        raise Http404

    context = {'content_type': ct, 'entries': ct.model_class().objects.all()}

    return render(request, 'mapper/content_type.html', context)

@login_required
@csrf_exempt
def model_search(request):
    if not request.user.is_staff:
        raise Http404
    
    results = [dict(content_type=content_type, results=content_type.model_class().objects.filter(**{"%s__icontains" % content_type.config['search_field']:request.GET['q']})) for content_type in get_content_types()]
    context = {"results": results}
    return render(request, 'mapper/search.html', context)

class EntryView(View, TemplateResponseMixin):
    template_name = 'mapper/entry.html'
    template_name_ajax = 'mapper/entry_list.html'

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(EntryView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        model_id = kwargs.get('model_id')
        entry_id = kwargs.get('entry_id')

    	ct = get_content_type(model_id)
        entry = ct.model_class().objects.get(pk=entry_id)

        context = {
            'content_type': ct,
            'entry': entry,
            }

        return context


    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if not request.user.is_staff:
            raise Http404        
        
        return self.render_to_response(context)


    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if not request.user.is_staff:
            raise Http404        
        
        service_slug = request.POST.get('slug', False)
        service_type = request.POST.get('service_type', False)

        context['service_slug'] = service_slug
        
        if service_slug:
            medias = [me.media for me in
                      MediaEntry.objects.filter(object_id=context['entry'].id, content_type=context['content_type'], media__service=service_slug, active=True).order_by('position')]
            context['service_slug'] = service_slug
        else:
            filters = {'object_id': context['entry'].id, 'content_type':context['content_type'], 'active': True, 'media__type': getattr(Media.TYPE_CHOICES,service_type.upper())}
            medias = [me.media for me in MediaEntry.objects.filter(**filters).order_by('position')]

        context['medias'] = medias

        return self.render_to_response(context)


    def get_template_names(self):
        return self.template_name if not self.request.is_ajax() else self.template_name_ajax


entry = EntryView.as_view()

class EditMediaFieldView(View):

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(EditMediaFieldView, self).dispatch(*args, **kwargs)
    
    def post(self, request, model_id, entry_id, media_id, *args, **kwargs):        
        edit_type = request.POST.get('edit_type', False)
        edit_text = request.POST.get('text', False)
	content_type = ContentType.objects.get(pk=model_id)

        if edit_type and media_id:
            kwargs = dict(media=Media.objects.get(pk=media_id),content_type=content_type,object_id=entry_id)
	    try:
		entry = MediaEntry.objects.get(**kwargs)
	    except MediaEntry.DoesNotExist:
		kwargs['user'] = request.user
		kwargs['active'] = False
		entry = MediaEntry.objects.create(**kwargs)

        if edit_type == "edit_title":
            entry.name = edit_text
            entry.save()
        elif edit_type == "edit_description":
            entry.description = edit_text
            entry.save()
        elif edit_type == "media_type":
            media_type = get_object_or_404(MediaType, name=edit_text)
            entry.media_type = media_type
            entry.save()
        return HttpResponse('OK')

edit_media_field = EditMediaFieldView.as_view()

class RollbackMediaFieldView(View):

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(RollbackMediaFieldView, self).dispatch(*args, **kwargs)
    
    def post(self, request, site_id, entry_id, media_id, *args, **kwargs):        
        original = request.POST.get('original', False)

        entry = MediaEntry.objects.get(media=Media.objects.get(pk=media_id), entry=Entry.objects.get(pk=entry_id))
        if original == "original_title":
            entry.name = ''
            entry.save()
        elif original == "original_description":
            entry.description = ''
            entry.save()
        return HttpResponse('OK')

rollback_media_field = RollbackMediaFieldView.as_view()

class EntryServiceSearchView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(EntryServiceSearchView, self).dispatch(*args, **kwargs)

    def post(self, request, model_id, entry_id):
        service_slug = request.POST.get('service_slug', False)
        action = request.POST.get('action', False)
        keyword = request.POST.get('keyword', False)
        search_type = request.POST.get('search_type', False)
        content_type = get_object_or_404(ContentType, pk=model_id)
        
        if not request.user.is_staff:
            raise Http404   

        page = int(request.POST.get('num', 1))
        if not (service_slug or action or keyword):
            return HttpResponse("{'error' :  Service, Action or Keyword not found'}")

        entry = content_type.model_class().objects.get(pk=entry_id)
        service = get_service_from_slug(service_slug)
        service.record_results = True

        if action == "keyword":
            res = service.search_by_keyword(keyword, page=page, entry=entry, return_objects=True)
            search_type = "media"
        elif action == "user":
            if search_type == "media":
                res = service.search_by_username(keyword, page=page, entry=entry, return_objects=True)
            else:
                res = service.search_albums_by_username(keyword, page=page, entry=entry, return_objects=True)

        if page * service.api.NB_RESULTS_PER_PAGE < res['index']['total_results']:
            next_page = page + 1
        else:
            next_page = False

        context = {"results": res, "entry": entry, "service": service, "action": action, "keyword": keyword,
                   "page": page, "next_page": next_page, "search_type": search_type, "content_type": content_type }

        return render(request, 'mapper/results/results_%s.html' % search_type, context)

entry_service_search = EntryServiceSearchView.as_view()

class EntryFromAlbumServiceSearchView(View):
    def get(self, request, site_id, entry_id, service_id, object_id):
        action = "album"

        website = get_object_or_404(Site, pk=site_id)
        entry = get_object_or_404(Entry, pk=entry_id)
        service = get_object_or_404(Service, pk=service_id)
        service.record_results = True

        res = service.search_by_album_id(object_id)

        return render(request, 'mapper/results/results_media.html', {
            "results": res,
            "entry": entry,
            "service": service,
            "action": action,
            'website': website
        })

entry_from_album_service_search = EntryFromAlbumServiceSearchView.as_view()

TYPE_ID_TO_SLUG = {1:'photo', 2:'video'}

class EntryPreviewView(View):
    def get(self, request, model_id, entry_id, service_slug, object_id):
        content_type = get_object_or_404(ContentType, pk=model_id)
        service = get_service_from_slug(service_slug)
        entry = get_object_or_404(content_type.model_class(), pk=entry_id)
        object = service.get_object(object_id)

        if not request.user.is_staff:
            raise Http404 

        try:
            media_entry = MediaEntry.objects.get(media=object, content_type=content_type, object_id=entry.id)
        except MediaEntry.DoesNotExist:
            media_entry = None

        media_types = MediaType.objects.all()

        return render(request, 'mapper/results/%s_preview.html' % TYPE_ID_TO_SLUG[object.type], {
            "entry": entry,
            "object": object,
            'content_type': content_type,
            'service': service,
            'media_entry': media_entry,
            'media_types': media_types,
            })

entry_preview = EntryPreviewView.as_view()

class AddMediaView(View):
    def get(self, request, model_id, entry_id, media_id):
	content_type = ContentType.objects.get(pk=model_id)
        entry = get_object_or_404(content_type.model_class(), pk=entry_id)
        media = get_object_or_404(Media, pk=media_id)

        if not request.user.is_staff:
            raise Http404 
        try:
            media_entry = MediaEntry.objects.get(content_type=content_type, object_id=entry.id, media=media)
        except MediaEntry.DoesNotExist:
            media_entry = MediaEntry.objects.create(content_object=entry, media=media, user=request.user, active=True)
        else:
            if not media_entry.active:
                media_entry.active = True
                media_entry.save()
        finally:
            media_entry.position = 99999
            media_entry.save()

        return HttpResponse("{'success' : 'This media is now associated to %s'}" % entry.name)

add_media = AddMediaView.as_view()

class RemoveMediaView(View):
    def get(self, request, site_id, entry_id, media_id):
        entry = get_object_or_404(Entry, pk=entry_id)
        media = get_object_or_404(Media, pk=media_id)

        media_entry = get_object_or_404(MediaEntry, entry=entry, media=media)

        media_entry.active = False
        media_entry.save()

        return HttpResponse("{'success' : 'This media is now unlinked from %s'}" % entry.name)

remove_media = RemoveMediaView.as_view()





class EntrySortView(View):
    template_name = 'mapper/entry.html'
    template_name_ajax = 'mapper/entry_list.html'

    
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(EntrySortView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        model_id = kwargs.get('model_id')
        entry_id = kwargs.get('entry_id')

        content_type = get_object_or_404(ContentType, pk=model_id)
        entry = get_object_or_404(content_type.model_class(), pk=entry_id)
        

        context = {
            'content_type': content_type,
            'entry': entry,
            'entry_id': entry_id
        }

        return context


    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if not request.user.is_staff:
            raise Http404        
        
        return render(request, context)


    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if not request.user.is_staff:
            raise Http404        
        
        service_id = int(request.POST.get('service_id', False))
        service_type = request.POST.get('service_type', False)

        order = request.POST.get('order', False)

        order_array = order.split('-')
        
        for i in range(len(order_array)):
            if order_array[i] != "":
                media_entry = get_object_or_404(MediaEntry, media=order_array[i], content_type=context['content_type'], object_id=context['entry_id'])
                media_entry.position = i
                media_entry.save()

        context['service_id'] = service_id
        return render(request, 'mapper/entry_list.html', context)


    def get_template_names(self):
        return self.template_name if not self.request.is_ajax() else self.template_name_ajax



entry_sort = EntrySortView.as_view()
