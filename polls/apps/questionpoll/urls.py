from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    IndexView,
    VoteView,
    ResultsView,
    PollEdit,

    FetchPollsView
)

urlpatterns = [
    url(r'^/?$', IndexView.as_view(), name="index"),
    url(r'^api/polls_index/?$', FetchPollsView.as_view(), name="fetch_all"),
    url(r'^(?P<id>\d+)/vote/?$', VoteView.as_view(), name="vote"),
    url(r'^(?P<pk>\d+)/results/?$', ResultsView.as_view(), name="results"),
    url(r'^(?P<pk>\d+)/edit/?$', PollEdit.as_view(), name="edit"),
]
