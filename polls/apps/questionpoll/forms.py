from __future__ import unicode_literals

from django import forms

from .models import Question


class VoteForm(forms.Form):
    choice = forms.ChoiceField(
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')

        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['choice'].choices =  map(
            lambda x:
            (x.id, x.answer_text),
            question.answers.all()
        )
