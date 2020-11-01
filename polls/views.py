"""The view configuration for Django polls app."""
import logging
from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from .models import Question, Choice, Vote

from django.views import generic

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(generic.ListView):
    """Class that contains configuration for index page."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return all last published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:]


class DetailView(generic.DetailView):
    """Class that contains configuration for detail page."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Return any questions that aren't published."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """Class that contains configuration for result page."""

    model = Question
    template_name = 'polls/results.html'


def polls_check_expire(request, question_id):
    """Check polls mechanism for polls app."""
    question = Question.objects.get(pk=question_id)
    if not question.can_vote():
        messages.warning(request,
                         "Poll expired!, please choose another question")
        return redirect('polls:index')
    else:
        return render(request, 'polls/detail.html', {'question': question, })


@login_required()
def vote(request, question_id):
    """
    Vote for each question by using question_id.
    """

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        Vote.objects.update_or_create(user=request.user, question=question, defaults={'choice': selected_choice})
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_passwd = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_passwd)
            login(request, user)
            return redirect('polls')
        # what if form is not valid?
        # we should display a message in signup.html
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
