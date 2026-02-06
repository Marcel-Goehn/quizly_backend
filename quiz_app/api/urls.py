from django.urls import path
from .views import QuizCreateView, QuizListView, QuizRetrieveUpdateDestroyView

urlpatterns = [
    path("createQuiz/", QuizCreateView.as_view(), name="create-quiz"),
    path("quizzes/", QuizListView.as_view(), name="quiz-list"),
    path("quizzes/<int:pk>/", QuizRetrieveUpdateDestroyView.as_view(), name="quiz-detail")
]
