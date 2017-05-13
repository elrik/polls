from __future__ import unicode_literals

from rest_framework import viewsets

from .serializers import QuestionSerializer, AnswerSerializer
from .models import Answer, Question


class QuestionViewset(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewset(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
