from django.contrib import admin
from mapper.models import *

admin.site.register(Media, admin.ModelAdmin)
admin.site.register(MediaEntry, admin.ModelAdmin)
admin.site.register(MediaType, admin.ModelAdmin)
admin.site.register(Keyword, admin.ModelAdmin)
