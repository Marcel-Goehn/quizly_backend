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


class CreateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "question_title", "question_options", "answer",
                  "created_at", "updated_at"]
        read_only_fields = ["id", "created_at"]

    def validate_question_options(self, value):
        if len(value) != 4:
            raise serializers.ValidationError(
                "Each question needs to have exactly 4 answer options.")
        return value

    def validate(self, attrs):
        for option in attrs["question_options"]:
            if attrs["answer"] == option:
                return attrs
        raise serializers.ValidationError(
            {"error": "The answer is nowhere to be found in the options"}
        )


class CreateQuizSerializer(serializers.ModelSerializer):

    questions = CreateQuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "description", "created_at",
                  "updated_at", "video_url", "questions"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_description(self, value):
        if len(value) > 150:
            raise serializers.ValidationError(
                "The maximum character length of the description is set to a maximum of 150.")
        return value

    def validate_questions(self, value):
        if len(value) != 10:
            raise serializers.ValidationError(
                "A quiz should always consist of 10 Questions.")
        return value

    def create(self, validated_data):
        user = validated_data.get("user")
        quiz_title = validated_data.get("title")
        quiz_description = validated_data.get("description")
        quiz_video_url = validated_data.get("video_url")
        quiz = Quiz.objects.create(user=user,
                                   title=quiz_title,
                                   description=quiz_description,
                                   video_url=quiz_video_url)
        for question in validated_data.get("questions"):
            Question.objects.create(quiz=quiz, question_title=question.get("question_title"),
                                    question_options=question.get(
                                        "question_options"),
                                    answer=question.get("answer"))
        return quiz
    

class ListRetrieveQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "question_title", "question_options", "answer"]
        read_only_fields = ["id", "question_title", "question_options", "answer"]
    

class ListRetrieveUpdateQuizSerializer(serializers.ModelSerializer):

    questions = ListRetrieveQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "description", "created_at", "updated_at",
                  "video_url", "questions"]
        read_only_fields = ["id", "created_at", "updated_at", "video_url"]