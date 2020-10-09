"""Contain question and choice class for Django polls application."""

import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """question class for  Django polls application."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('Date that polls expires')

    def __str__(self):
        """Return a string represent for question class."""
        return self.question_text

    def is_published(self):
        """Check question that published or not."""
        now = timezone.now()
        if now >= self.pub_date:
            return True
        else:
            return False

    def can_vote(self):
        """Check question that can vote or not."""
        now = timezone.now()
        if self.pub_date <= now <= self.end_date:
            return True
        else:
            return False

    def was_published_recently(self):
        """Check question that published recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'end_date'
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """choice class for  Django polls application."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return a string represent for choice class."""
        return self.choice_text
