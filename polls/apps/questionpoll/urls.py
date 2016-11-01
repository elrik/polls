from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    IndexView,
    VoteView,
    ResultsView,
)

urlpatterns = [
    url(r'^/?$', IndexView.as_view(), name="index"),
    url(r'^(?P<id>\d+)/vote/?$', VoteView.as_view(), name="vote"),
    url(r'^(?P<pk>\d+)/results/?$', ResultsView.as_view(), name="results"),
]
