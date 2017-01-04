from __future__ import unicode_literals

import json

from channels import Group

from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=255)

    def __str__(self):
        return self.question

    def get_channel_group_result(self):
        return "poll-result-%s" % (self.pk)

    def get_channel_groups(self):
        return [
            "poll-result-%s" % (self.pk),
        ]

    def to_dict(self):
        answers = [
            answer.to_dict()
            for answer in self.answers.all()
        ]

        answer_graph_data = [
            [answer.answer_text, answer.votes]
            for answer in self.answers.all()
        ]

        return {
            'id': self.pk,
            'question': self.question,
            'answers': answers,
            'answer_graph_data': answer_graph_data,
        }


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers')
    answer_text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return "%s: %s" % (self.question, self.answer_text)

    def add_vote(self):
        self.votes = models.F('votes') + 1
        self.save()

        # Broadcast update to the appropriate group
        channel_group = Group(self.question.get_channel_group_result())

        data = self.question.to_dict()

        data.update({
            'action': 'update-results',
        })

        channel_group.send({
            "text": json.dumps(data)
        })

    def to_dict(self):
        return {
            'id': self.pk,
            'answer_text': self.answer_text,
            'votes': self.votes,
        }
