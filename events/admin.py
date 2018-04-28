from django.contrib import admin
from .models import Event, Talk, Speaker

admin.site.register(Event)
admin.site.register(Talk)
admin.site.register(Speaker)