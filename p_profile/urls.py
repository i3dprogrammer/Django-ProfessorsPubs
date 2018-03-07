from django.conf.urls import url
from .views import CreateProfessorProfileView, ProfessorProfileView

app_name = 'p_profile'

urlpatterns = [
    url(r'^create/$', CreateProfessorProfileView.as_view(), name='create'),
    url(r'^view/$', ProfessorProfileView.as_view(), name='view'),
    #url(r'^edit/$', CreateProfessorProfileView.as_view(), name='edit', kwargs={'edit':True}),
]