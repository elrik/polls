from __future__ import unicode_literals

from django.contrib import admin

from .models import Question, Answer


admin.site.register(Answer)
admin.site.register(Question)