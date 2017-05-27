from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from dry_rest_permissions.generics import DRYPermissions

from .serializers import QuestionSerializer, AnswerSerializer
from .models import Answer, Question


class CustomAuth(SessionAuthentication):

    def enforce_csrf(self, request):
        return None


class QuestionViewset(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = (CustomAuth,)
    permission_classes = (DRYPermissions,)


class AnswerViewset(viewsets.ModelViewSet):
    queryset = Answer.objects.all()

    serializer_class = AnswerSerializer
    authentication_classes = (CustomAuth,)
    permission_classes = (DRYPermissions,)

    @detail_route(methods=['post', 'put'])
    def vote(self, request, pk=None):
        answer = self.get_object()
        answer.add_vote()

        return Response(answer.to_dict())
