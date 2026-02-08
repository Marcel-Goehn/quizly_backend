from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import YouTubeURLSerializer, CreateQuizSerializer, ListRetrieveUpdateQuizSerializer
from .permissions import IsOwner
import os
import yt_dlp
import whisper
import json
from google import genai
from dotenv import load_dotenv
from rest_framework import status
from quiz_app.models import Quiz
from drf_spectacular.utils import extend_schema, extend_schema_view

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
        self.download_audio(data.get("url"))
        transcription_result = self.transcribe_audio()
        generated_quiz = self.create_quiz(transcription_result)
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

    def download_audio(self, id):
        url = f"https://www.youtube.com/watch?v={id}"
        tmp_filename = "quiz_app/audio/audio.aac"
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": tmp_filename,
            "quiet": True,
            "noplaylist": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(url)

    def transcribe_audio(self):
        model = whisper.load_model("turbo")
        result = model.transcribe("quiz_app/audio/audio.aac")
        return result

    def create_quiz(self, transcript):
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=f"""
                Based on the following transcript, generate a quiz in valid JSON format.
                The quiz must follow this exact structure:
                {{"title": "Create a concise quiz title based on the topic of the transcript.",
                "description": "Summarize the transcript in no more than 150 characters. 
                Do not include any quiz questions or answers.",
                "questions": [
                {{"question_title": "The question goes here.",
                "question_options": ["Option A", "Option B", "Option C", "Option D"],
                "answer": "The correct answer from the above options"}},
                ...
                (exactly 10 questions)]}}
                Requirements:
                - Each question must have exactly 4 distinct answer options.
                - Only one correct answer is allowed per question, 
                and it must be present in 'question_options'.
                - The output must be valid JSON and parsable as-is 
                (e.g., using Python's json.loads).
                - Do not include explanations, comments, or any text outside the JSON.
                This is the following Transcript: {transcript}
            """
        )
        cleaned_response = json.loads(response.text)
        return cleaned_response


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
