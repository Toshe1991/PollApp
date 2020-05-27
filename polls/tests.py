import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# Create your tests here.


class QuestionModelTest(TestCase):

    def test_was_published_recently_with_overflow(self):
        time = timezone.now() + datetime.timedelta(days=1)
        f_question = Question(creation_date=time)

        self.assertIs(f_question.was_published_recently(), False)

    def test_was_published_recently_with_negative(self):
        time = timezone.now() - datetime.timedelta(days=2)
        old_question = Question(creation_date=time)

        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent(self):
        time = timezone.now() - datetime.timedelta(hours=5)
        recent_question = Question(creation_date=time)

        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, creation_date=time)


class QuestionIndexViewTest(TestCase):

    def test_no_question(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        create_question(question_text="Past Question", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],
                                 ['<Question: Past Question>'])

    def test_future_question(self):
        create_question(question_text="Future Question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past(self):
        create_question(question_text="Past Question", days=-5)
        create_question(question_text="Future Question", days=1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [
            '<Question: Past Question>'
        ])

    def test_two_past_questions(self):
        create_question(question_text="Past Question 5", days=-5)
        create_question(question_text="Past Question 2", days=-2)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past Question 2>', '<Question: Past Question 5>']
        )


class QuestionDetailViewIndex(TestCase):

    def test_future_question(self):
        future_question = create_question(question_text="Future Question", days=1)
        response = self.client.get(reverse("polls:detail", args=(future_question.id, )))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text="Past Question", days=-2)
        response = self.client.get(reverse("polls:detail", args=(past_question.id, )))
        self.assertContains(response, past_question.question_text)
