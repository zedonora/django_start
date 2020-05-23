import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question
# Create your tests here.


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')

        self.assertQuerysetEqual(response.context['lastest_question_list'], [])

    def test_past_question(self):
        create_question(question_text='Past question.', days=-30)
        response = self.client.get(reverse('polls;index'))
        self.assertQuerysetEqual(response.context['lastest_question_list'], [
                                 '<Question: Past question.>'])

    def test_future_question(self):
        create_question(question_text='Future question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['lastest_question_list'], [])

    def test_future_question_and_past_question(self):
        create_question(question_text='Past question.', days=-30)
        create_question(question_text='Future question.', days=30)
        resposne = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(resposne.context['lastest_question_list'], [
                                 '<Question: Past question.>'])

    def test_two_past_questions(self):
        create_question(question_text='Past question1.', days=-30)
        create_question(question_text='Past question2.', days=-5)
        resposne = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(resposne.context['lastest_question_list'], [
                                 '<Question: Past question2.>', '<Question: Past question1.>'])
