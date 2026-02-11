import re
from rest_framework import serializers
from quiz_app.models import Quiz, Question


class YouTubeURLSerializer(serializers.Serializer):
    """
    This serializer is only used for validating the provided url.
    It also extracts the video ID with the help of regex.
    """
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
    """
    Used as a nested serializer.
    """
    class Meta:
        model = Question
        fields = ["id", "question_title", "question_options", "answer",
                  "created_at", "updated_at"]
        read_only_fields = ["id", "created_at"]

    def validate_question_options(self, value):
        """
        If a question has not exactly 4 possible answer options,
        a validation error will be raised.
        """
        if len(value) != 4:
            raise serializers.ValidationError(
                "Each question needs to have exactly 4 answer options.")
        return value

    def validate(self, attrs):
        """
        Makes sure that the answer is also to be found in the question options.
        If not, a validation error will be raised.
        """
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
        """
        Makes sure that the description of the quiz does not exceed a maximum of 150 character.
        If it does, a validation error will be raised.
        """
        if len(value) > 150:
            raise serializers.ValidationError(
                "The maximum character length of the description is set to a maximum of 150.")
        return value

    def validate_questions(self, value):
        """
        Makes sure that the quiz contains exactly 10 questions.
        If it doesn't, a validation error will be raised.
        """
        if len(value) != 10:
            raise serializers.ValidationError(
                "A quiz should always consist of 10 Questions.")
        return value

    def create(self, validated_data):
        """
        Custom create method. Has to be done, or the nested writing (questions)
        into the database would not be possible.
        """
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
        read_only_fields = ["id", "question_title",
                            "question_options", "answer"]


class ListRetrieveUpdateQuizSerializer(serializers.ModelSerializer):

    questions = ListRetrieveQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "description", "created_at", "updated_at",
                  "video_url", "questions"]
        read_only_fields = ["id", "created_at", "updated_at", "video_url"]

    def validate(self, attrs):
        """
        Check if fields other than title and description are tried to be updated.
        If the title or description are not provided the attrs dict will be empty, so a length of 0
        will be returned
        """
        if len(attrs) == 0:
            raise serializers.ValidationError({
                "error": "Only quiz title and description can be updated via PATCH."
            })
        return attrs
