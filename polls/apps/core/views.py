from __future__ import unicode_literals

from django.views.generic import TemplateView


class WelcomeView(TemplateView):
    template_name = 'core/welcome.html'
