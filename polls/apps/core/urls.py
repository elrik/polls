# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import (
    WelcomeView,
)

urlpatterns = [
    url(r'^/?$', WelcomeView.as_view(), name="welcome"),
]
