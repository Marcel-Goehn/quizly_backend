import re

from rest_framework import serializers

from quiz_app.models import Quiz, Question


class YouTubeURLSerializer(serializers.Serializer):
    url = serializers.URLField(allow_blank=False, required=True)

    def validate_url(self, value):
        regex = re.compile(
            r'(?:https?://)?(?:www\.)?'
            r'(?:youtube\.com/(?:watch\?v=|shorts/)|youtu\.be/)'
            r'([A-Za-z0-9_-]{11})'
        )
        id = regex.search(value)
        if id is None:
            raise serializers.ValidationError(
                "Couldn't extract YouTube video ID from the provided URL. Please try again."
            )
        return id.group(1)


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
