from __future__ import unicode_literals

import json

from django.urls import reverse

from channels.generic.websockets import WebsocketConsumer

from .models import Question  # , Answer
from .forms import VoteForm


class MessageParser(object):
    def parse_message(self, message):
        try:
            return json.loads(message)

        except Exception as e:
            print e
            return None


class PollResultsConsumer(MessageParser, WebsocketConsumer):
    """
    Polls consumer
    """

    http_user = True

    strict_ordering = False
    slight_ordering = False

    def connection_groups(self, poll_id, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        return ["poll-result-%s" % (poll_id)]

    def connect(self, message, **kwargs):
        poll = Question.objects.get(pk=kwargs.get('poll_id', ""))
        self.send(json.dumps(poll.to_dict()))

    def receive(self, text=None, bytes=None, **kwargs):
        print self.message.user.is_superuser

    def disconnect(self, message, **kwargs):
        pass


class PollEditConsumer(MessageParser, WebsocketConsumer):
    http_user = True

    strict_ordering = False
    slight_ordering = False

    def connection_groups(self, poll_id, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        return ["poll-edit-%s" % (poll_id)]

    def connect(self, message, **kwargs):
        poll = Question.objects.get(pk=kwargs.get('poll_id', ""))
        self.send(json.dumps(poll.to_dict()))

    def receive(self, text=None, bytes=None, **kwargs):
        print self.message.user.is_superuser
        print text

        data = self.parse_message(text)

        if self.message.user.has_perm("questionpoll.change_question") and data:
            poll = Question.objects.get(pk=kwargs.get('poll_id', ""))

            if data.get('action', None) == "update-poll":
                poll.question = data['data'].get('question', poll.question)

                poll.save()

            elif data.get('action', None) == "update-answer":
                answer = poll.answers.filter(
                    pk=data['data'].get('id', None)
                )

                answer.update(answer_text=data['data'].get('answer_text'))

            self.send(json.dumps({
                'action': 'update-poll',
                'status': "success",
                'poll': poll.to_dict(),
            }))

        else:
            self.send(json.dumps({
                'status': "error",
                'type': 'permission',
            }))

    def disconnect(self, message, **kwargs):
        pass


class PollVoteConsumer(MessageParser, WebsocketConsumer):
    http_user = True

    strict_ordering = False
    slight_ordering = False

    def connection_groups(self, poll_id, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        res = [
            "poll-vote-%s" % (poll_id),
            "poll-result-%s" % (poll_id),
        ]

        print res

        return res

    def connect(self, message, **kwargs):
        poll = Question.objects.get(pk=kwargs.get('poll_id', ""))
        self.send(json.dumps(poll.to_dict()))

    def receive(self, text=None, bytes=None, poll_id=None, **kwargs):
        poll = Question.objects.get(pk=poll_id)

        # We only allow for json here
        data = self.parse_message(text)
        print data

        if data:
            form = VoteForm(data['data'], question=poll)
            if form.is_valid():
                answer_id = form.cleaned_data.get('choice')
                answer = answer = poll.answers.get(pk=answer_id)
                answer.add_vote()

                # self.send(text=json.dumps(poll.to_dict()))
                self.send(text=json.dumps({
                    'status': "ok",
                    'redirect_url':
                        reverse('questionpoll:results', args=[poll.id]),
                    'action': 'vote',
                }))

            else:
                self.send(text=json.dumps({
                    'status': "error",
                    'action': 'vote',
                    'errors': form.errors,
                }))

    def disconnect(self, message, **kwargs):
        pass
