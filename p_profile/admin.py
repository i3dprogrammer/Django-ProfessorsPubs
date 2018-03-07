from django.contrib import admin
from .models import Department, Affiliation, ProfessorProfile

admin.site.register(Department)
admin.site.register(Affiliation)
admin.site.register(ProfessorProfile)