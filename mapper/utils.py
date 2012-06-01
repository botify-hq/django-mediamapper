from django.conf import settings
from django.contrib.contenttypes.models import ContentType

def get_content_types():
    models = []
    for m, config in settings.MEDIA_MAPPER_MODELS.iteritems():
	try:
	    app_label, model = m.split('.')
	    ct = ContentType.objects.get(app_label=app_label, model=model)
	    ct.config = config
            models.append(ct)
	except:
	    pass
    return models

def get_content_type(id):
    for ct in get_content_types():
        if ct.id == int(id):
	    return ct
    return
