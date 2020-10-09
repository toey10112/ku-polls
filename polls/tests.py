"""Unittests for Django polls application."""
import datetime

from django.test import TestCase

from django.utils import timezone
from .models import Question
from django.urls import reverse


def create_question(question_text, days,end_date):
    """
    Create a question.

    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    time2 = timezone.now() + datetime.timedelta(days=end_date)

    return Question.objects.create(question_text=question_text, pub_date=time,end_date = time2)


class QuestionModelTests(TestCase):
    """Class that contains a unittest for Model in django polls app."""

    def test_is_published_with_old_question(self):
        """Test is_published work with old_question."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertTrue(old_question.is_published())

    def test_is_published_with_recent_question(self):
        """Test is_published work with recent_question."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        recent_question = Question(pub_date=time)
        self.assertTrue(recent_question.is_published())

    def test_is_published_with_future_question(self):
        """Test is_published work with future_question."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.is_published())

    def test_can_vote_with_old_question(self):
        """Test can_vote work with old_question."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertTrue(old_question.can_vote())

    def test_can_vote_with_recent_question(self):
        """Test can_vote work with recent_question."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        recent_question = Question(pub_date=time)
        self.assertTrue(recent_question.can_vote())

    def test_can_vote_with_future_question(self):
        """Test can_vote work with future_question."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertTrue(future_question.can_vote())

    def test_was_published_recently_with_future_question(self):
        """Test was published recently with future question."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """Test was published recently with old question."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """Test was published recently with recent question."""
        time = timezone.now() - datetime\
            .timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    """Class that contains a unittest for index view."""

    def test_no_questions(self):
        """Test app can work with no question."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Test past question can work in app."""
        create_question(question_text="Past question.", days=-30,end_date=-15)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """Test app can work with future question(cant see question)."""
        create_question(question_text="Future question.", days=30,end_date=45)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """Test future question and past question can work."""
        create_question(question_text="Past question.", days=-30,end_date=-15)
        create_question(question_text="Future question.", days=30,end_date=45)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """Test two past question can work."""
        create_question(question_text="Past question 1.", days=-30,end_date=-15)
        create_question(question_text="Past question 2.", days=-5,end_date=-1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionDetailViewTests(TestCase):
    """Class that contains a unittest for detail view in django polls app."""

    def test_future_question(self):
        """Test view can work with future question."""
        future_question = \
            create_question(question_text='Future question.',
                            days=5,end_date=15)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """Test can work with past question."""
        past_question = \
            create_question(question_text='Past Question.',
                            days=-5,end_date=-1)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

# Response Codes:1xx Information100 Continue
# 2xx Success200 OK
# 201 Created (a new resource was successfully created)
# 202 Accepted (I'll process your request later)
# 3xx Redirection
# 301 Moved Permanently. New URL in Location header.
# 302 Moved Temporarily. New URL in Location header.
# 303 Redirect and change POST to GET method
# 304 Not Modified ("Look in your cache, stupid")
# Error Response Codes
# 4xx Client Error
# 400 Bad Request
# 401 Not Authorized (client not authorized to do this)
# 404 Not Found
# 5xx Server Error
# 500 Internal Server Error  (application error, config prob.)
# 503 Service Unavailable
