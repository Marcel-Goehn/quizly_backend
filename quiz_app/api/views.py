from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import YouTubeURLSerializer
import yt_dlp


class QuizView(APIView):
    def post(self, req):

        """
        First part of the view. This part is dedicated to download the audio file from the
        specific YouTube video.

        ydl_opts explained:
            -format: specifies the desired output format
            -outtmpl: sets the saving location of the generated audio file
            -quiet: ...
            -noplaylist: Makes sure that not a whole playlist will be downlaoded
        """
        serializer = YouTubeURLSerializer(data=req.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
        url = f"https://www.youtube.com/watch?v={data.get("url")}"
        tmp_filename = "quiz_app/audio/audio.webm"

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": tmp_filename,
            "quiet": True,
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(url)

        """
        Second part of the view. This part is dedicated to transcribe the audio file
        into text.
        """
        
        return Response("Response!")
