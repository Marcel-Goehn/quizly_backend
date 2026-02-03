from django.urls import path
from .views import QuizView

urlpatterns = [
    path("createQuiz/", QuizView.as_view(), name="create-quiz")
]
