from rest_framework import serializers

from quiz_app.models import Quiz, Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "question_title", "question_options", "answer", 
                  "created_at", "updated_at"]
        read_only_fields = ["id", "created_at"]


class CreateQuizSerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "description", "created_at", 
                  "video_url", "questions"]
        read_only_fields = ["id", "created_at"]