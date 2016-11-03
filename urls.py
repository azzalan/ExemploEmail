from django.conf.urls import patterns, url, include
from django.conf import settings
from app.views import *

urlpatterns = [
    url(r'^membros/$',
            MembrosView.as_view(),
            name='membros'),
]
