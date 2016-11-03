from django.conf.urls import patterns, url, include
from django.conf import settings
from app.views import *

urlpatterns = [
    url(r'^caminho-de-url/resto-do-caminho/$',
            EmailView.as_view(),
            name='nome_da_url'),
]
