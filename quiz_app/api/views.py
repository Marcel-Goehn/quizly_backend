from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import YouTubeURLSerializer
import yt_dlp
import whisper


class QuizView(APIView):
    def post(self, req):
        serializer = YouTubeURLSerializer(data=req.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
        self.download_audio(data.get("url"))
        transcription_result = self.transcribe_audio()
        return Response(transcription_result["text"])

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
