from __future__ import unicode_literals


from django.views.generic import (
    ListView,
    UpdateView,
    DetailView,
    FormView,
)
from django.urls import reverse

from .models import Question
from .forms import VoteForm, AnswerForm


class IndexView(ListView):
    model = Question
    template_name = 'questionpoll/index.html'


class VoteView(FormView):
    template_name = 'questionpoll/vote.html'
    form_class = VoteForm

    def get_form_kwargs(self):
        kwargs = super(VoteView, self).get_form_kwargs()
        kwargs.update({
            'question': self.get_question_object(),
        })

        return kwargs

    def get_question_object(self):
        question_id = self.kwargs.get('id')
        self.object = Question.objects.get(pk=question_id)

        return self.object

    def form_valid(self, form):
        """
        Manipulate data here :o)
        """
        answer_id = form.cleaned_data.get('choice')
        answer = self.object.answers.get(pk=answer_id)
        answer.add_vote()

        print self.object.to_dict()

        return super(VoteView, self).form_valid(form)

    def get_success_url(self):
        return reverse('questionpoll:results', args=[self.object.id])


class ResultsView(DetailView):
    model = Question
    template_name = 'questionpoll/results.html'


class PollEdit(UpdateView):
    model = Question
    template_name = 'questionpoll/edit.html'
    fields = ['question']

    def get_context_data(self, *args, **kwargs):
        context = super(PollEdit, self).get_context_data(*args, **kwargs)

        answer_forms = []

        for answer in self.object.answers.all():
            answer_forms.append(AnswerForm(instance=answer))

        context.update({
            'answer_forms': answer_forms,
        })

        # raise "Foo"

        return context
