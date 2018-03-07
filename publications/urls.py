from django.conf.urls import url
from .views import NewPublicationView, PublicationView

app_name = 'publications'

urlpatterns = [
    url(r'^new/$', NewPublicationView.as_view(), name='new'),
    url(r'^edit/(?P<pub_id>[0-9]+)/$', NewPublicationView.as_view(), name='edit'),
    url(r'view/(?P<pub_id>[0-9]+)/$', PublicationView.as_view(), name='view'),
]