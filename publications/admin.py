from django.contrib import admin
from .models import Publication, ResearchField

admin.site.register(ResearchField)
admin.site.register(Publication)