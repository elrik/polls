from __future__ import unicode_literals

from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=255)

    def __str__(self):
        return self.question


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers')
    answer_text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return "%s: %s" % (self.question, self.answer_text)

    def add_vote(self):
        self.votes = models.F('votes') + 1
        self.save()
