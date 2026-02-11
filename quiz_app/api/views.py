import os
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view
from .serializers import YouTubeURLSerializer, CreateQuizSerializer, ListRetrieveUpdateQuizSerializer
from .permissions import IsOwner
from quiz_app.models import Quiz
from quiz_app.functions import download_audio, transcribe_audio, create_quiz

load_dotenv()


class QuizCreateView(APIView):

    @extend_schema(
        description="Authentication required. Creates a Quiz in multiple steps. Step 1: Extracts audio from YouTube video. Step 2: Transcribes the audio into text. Step 3: Takes the generated text and inputs it into Gemini API to create a Quiz.",
        request=YouTubeURLSerializer,
        responses={201: CreateQuizSerializer}
    )
    def post(self, req):
        url_serializer = YouTubeURLSerializer(data=req.data)
        if url_serializer.is_valid(raise_exception=True):
            data = url_serializer.validated_data
        os.remove("quiz_app/audio/audio.aac")
        download_audio(data.get("url"))
        transcription_result = transcribe_audio()
        generated_quiz = create_quiz(transcription_result)
        quiz_information_dict = {
            "title": generated_quiz.get("title"),
            "description": generated_quiz.get("description"),
            "video_url": f"https://www.youtube.com/watch?v={data.get('url')}",
            "questions": generated_quiz.get("questions")
        }
        quiz_serializer = CreateQuizSerializer(data=quiz_information_dict)
        if quiz_serializer.is_valid(raise_exception=True):
            quiz_serializer.save(user=req.user)
            return Response(quiz_serializer.data, status=status.HTTP_201_CREATED)
        return Response(quiz_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    description="Authentication required. Returns a list of all quizzes that the authenticated users has created."
)
class QuizListView(ListAPIView):
    serializer_class = ListRetrieveUpdateQuizSerializer

    def get_queryset(self):
        return Quiz.objects.filter(user=self.request.user)


@extend_schema_view(
    get=extend_schema(
        description="Authentication required. Returns a specific quiz. User has to be the creator."
    ),
    put=extend_schema(
        description="PUT is not supported. Use PATCH instead."
    ),
    patch=extend_schema(
        description="Authentication required. User has to be the owner of the specific quiz. title and description can be updated."
    ),
    delete=extend_schema(
        description="Authentication required. User has to be the owner of the specific quiz. Deletes it permanently."
    )
)
class QuizRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Quiz.objects.all()
    serializer_class = ListRetrieveUpdateQuizSerializer
