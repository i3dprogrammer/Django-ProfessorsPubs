from django.conf.urls import url
from .views import LoginView
from django.contrib.auth.views import logout
app_name = 'accounts'

urlpatterns = [
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout, {'next_page': 'p_profile:view'}, name='logout')
]