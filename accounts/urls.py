from django.conf.urls import url
from .views import LoginView

app_name = 'accounts'

urlpatterns = [
    url(r'^$', LoginView.as_view(), name='login'),
]