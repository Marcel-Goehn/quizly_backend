from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from quiz_app.models import Quiz, Question


class QuizTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test.mail@testmail.com",
                                             password="test12345")
        
        self.user_two = User.objects.create_user(username="testusertwo",
                                                 email="testmail.two@gmail.com",
                                                 password="test12345")
        
        self.quiz = Quiz.objects.create(user=self.user, title="test title",
                                        description="test description for this quiz",
                                        video_url="https://www.youtube.com/watch?v=aXOChLn5ZdQ")
        
        self.question_one = Question.objects.create(quiz=self.quiz, question_title="question_one",
                                                    question_options=["1", "2", "3", "4"],
                                                    answer="1")
        
        self.question_two = Question.objects.create(quiz=self.quiz, question_title="question_two",
                                                    question_options=["1", "2", "3", "4"],
                                                    answer="1")
        
        self.question_three = Question.objects.create(quiz=self.quiz, question_title="question_three",
                                                    question_options=["1", "2", "3", "4"],
                                                    answer="1")
        
        self.question_four = Question.objects.create(quiz=self.quiz, question_title="question_four",
                                                    question_options=["1", "2", "3", "4"],
                                                    answer="1")
        
        self.question_five = Question.objects.create(quiz=self.quiz, question_title="question_five",
                                                    question_options=["1", "2", "3", "4"],
                                                    answer="1")
        
        self.question_six = Question.objects.create(quiz=self.quiz, question_title="question_six",
                                                    question_options=["1", "2", "3", "4"],
                                                    answer="1")
        
        self.question_seven = Question.objects.create(quiz=self.quiz, question_title="question_seven",
                                                    question_options=["1", "2", "3", "4"],
                                                    answer="1")
        
        self.question_eight = Question.objects.create(quiz=self.quiz, question_title="question_eight",
                                                    question_options=["1", "2", "3", "4"],
                                                    answer="1")
        
        self.question_nine = Question.objects.create(quiz=self.quiz, question_title="question_nine",
                                                    question_options=["1", "2", "3", "4"],
                                                    answer="1")
        
        self.question_ten = Question.objects.create(quiz=self.quiz, question_title="question_ten",
                                                    question_options=["1", "2", "3", "4"],
                                                    answer="1")
        
    def test_get_quizzes_successful(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("quiz-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_quizzes_not_authenticated(self):
        url = reverse("quiz-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_quiz_successful(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("quiz-detail", kwargs={"pk": self.quiz.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_quiz_not_authenticated(self):
        url = reverse("quiz-detail", kwargs={"pk": self.quiz.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_quiz_not_owner(self):
        self.client.force_authenticate(user=self.user_two)
        url = reverse("quiz-detail", kwargs={"pk": self.quiz.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_quiz_not_found(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("quiz-detail", kwargs={"pk": 327632})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_quiz_successfully(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("quiz-detail", kwargs={"pk": self.quiz.pk})
        data = {
            "title": "title changed",
            "description": "description changed"
        }
        response = self.client.patch(url, data, forma="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_quiz_not_successful(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("quiz-detail", kwargs={"pk": self.quiz.pk})
        data = {
            "video_url": "https://www.youtube.com/watch?v=7dqMSlv2jeA"
        }
        response = self.client.patch(url, data, forma="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_quiz_not_authenticated(self):
        url = reverse("quiz-detail", kwargs={"pk": self.quiz.pk})
        data = {
            "title": "title changed",
            "description": "description changed"
        }
        response = self.client.patch(url, data, forma="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_quiz_not_owner(self):
        self.client.force_authenticate(user=self.user_two)
        url = reverse("quiz-detail", kwargs={"pk": self.quiz.pk})
        data = {
            "title": "title changed",
            "description": "description changed"
        }
        response = self.client.patch(url, data, forma="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_quiz_not_found(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("quiz-detail", kwargs={"pk": 321098})
        data = {
            "title": "title changed",
            "description": "description changed"
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_quiz_successfully(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("quiz-detail", kwargs={"pk": self.quiz.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_quiz_not_authenticated(self):
        url = reverse("quiz-detail", kwargs={"pk": self.quiz.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_quiz_not_owner(self):
        self.client.force_authenticate(user=self.user_two)
        url = reverse("quiz-detail", kwargs={"pk": self.quiz.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_quiz_not_found(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("quiz-detail", kwargs={"pk": 213443})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)